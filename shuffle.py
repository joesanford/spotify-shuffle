import click

import spotify_utils as su

PLAYLIST_ID = '2uN3clGz8OFuoc6JjOwdNY'


@click.command()
def sync():
    sp = su.init_sp()

    saved_tracks = su.get_saved_tracks(sp)
    print(f'{len(saved_tracks)} saved tracks')

    playlist_tracks = su.get_playlist_tracks(sp, PLAYLIST_ID)
    print(f'{len(playlist_tracks)} playlist tracks')

    print('done syncing!')


@click.command()
def shuffle():
    sp = su.init_sp()

    saved_tracks = su.get_saved_tracks(sp)
    print(f'{len(saved_tracks)} saved tracks')

    su.shuffle_playlist(sp, saved_tracks, PLAYLIST_ID)

    print('done shuffling!')


@click.group()
def cli():
    pass


cli.add_command(sync)
cli.add_command(shuffle)

if __name__ == '__main__':
    cli()
