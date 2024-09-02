import os
import random

import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_SECRET')
REDIRECT_URI = 'http://127.0.0.1:8888'
CHUNK_SIZE = 100


def init_sp() -> spotipy.Spotify:
    sp_oauth=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-library-read, playlist-read-private, playlist-modify-private, playlist-modify-public',
        open_browser=False,
    )

    token_info = sp_oauth.get_cached_token()
    
    if not token_info or sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    sp = spotipy.Spotify(auth=token_info['access_token'])

    return sp

def print_progress(songs: list, res):
    if len(songs) % 250 == 0:
        print(f'{round(len(songs) / res.get("total") * 100, 1)}% fetched')

    if not res.get('next'):
        print('100% fetched')


def get_saved_tracks(sp: spotipy.Spotify) -> list:
    print('fetching saved tracks')
    songs = []
    offset = 0

    while True:
        res = sp.current_user_saved_tracks(limit=50, offset=offset)
        songs.extend([s.get('track').get('uri') for s in res.get('items')])
        offset += 50

        print_progress(songs, res)

        if not res.get('next'):
            break
    
    return songs


def get_playlist_tracks(sp: spotipy.Spotify, playlist: str) -> list:
    print('fetching playlist tracks')
    songs = []
    offset = 0

    while True:
        res = sp.playlist_items(playlist, limit=50, offset=offset)
        songs.extend([s.get('track').get('uri') for s in res.get('items')])
        offset += 50

        print_progress(songs, res)

        if not res.get('next'):
            break
    
    return songs


def sync_playlists(sp: spotipy.Spotify, saved_tracks: list, playlist_tracks: list):
    songs_to_add = [t for t in saved_tracks if t not in playlist_tracks]
    songs_to_remove = [t for t in playlist_tracks if t not in saved_tracks]

    print(f'{len(songs_to_add)} songs to add')
    print(f'{len(songs_to_remove)} songs to remove')

    if songs_to_add:
        sp.playlist_add_items(PLAYLIST_ID, songs_to_add)
    if songs_to_remove:
        sp.playlist_remove_all_occurrences_of_items(PLAYLIST_ID, songs_to_remove)

    return


def shuffle_playlist(sp: spotipy.Spotify, tracks: list, playlist: str):
    print('shuffling playlist')
    random.shuffle(tracks)

    tracks_to_delete = tracks[:]

    total_tracks_to_delete = len(tracks_to_delete)
    while tracks_to_delete:
        sp.playlist_remove_all_occurrences_of_items(playlist, tracks_to_delete[:CHUNK_SIZE])
        del tracks_to_delete[:CHUNK_SIZE]
        print(f'{round(100 - len(tracks_to_delete) / total_tracks_to_delete * 100, 1)}% deleted')

    print('done deleting')
    
    total_tracks = len(tracks)
    print(f'{total_tracks} to add')
    while tracks:
        sp.playlist_add_items(playlist, tracks[:CHUNK_SIZE])
        del tracks[:CHUNK_SIZE]
        print(f'{round(100 - len(tracks) / total_tracks * 100, 1)}% added')

    print('done repopulating')