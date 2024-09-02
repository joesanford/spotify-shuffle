import click

import spotify_utils as su

PLAYLIST_ID = '2uN3clGz8OFuoc6JjOwdNY'


def sync():
    sp = su.init_sp()

    saved_tracks = su.get_saved_tracks(sp)
    print(f'{len(saved_tracks)} saved tracks')

    playlist_tracks = su.get_playlist_tracks(sp, PLAYLIST_ID)
    print(f'{len(playlist_tracks)} playlist tracks')

    su.sync_playlists(sp, saved_tracks, playlist_tracks, PLAYLIST_ID)

    print('done syncing!')

def shuffle():
    sp = su.init_sp()

    saved_tracks = su.get_saved_tracks(sp)
    print(f'{len(saved_tracks)} saved tracks')

    su.shuffle_playlist(sp, saved_tracks, PLAYLIST_ID)

    print('done shuffling!')
