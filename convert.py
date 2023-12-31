import pandas as pd
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
import argparse
from bs4 import BeautifulSoup
import requests

load_dotenv()

scope = "user-library-read,playlist-modify-public,playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# https://github.com/spotipy-dev/spotipy/blob/master/examples/create_playlist.py
def get_args():
    parser = argparse.ArgumentParser(description='Creates a playlist for user')
    parser.add_argument('-p', '--playlist', required=True,
                        help='Name of Playlist')
    parser.add_argument('-d', '--description', required=False, default='',
                        help='Description of Playlist')
    return parser.parse_args()

# Return the URI of the first song returned when searching the song title and artist name
def find_song(song, artist):
    return sp.search(song + artist, type='track')['tracks']['items'][0]['uri']

def main():
    args = get_args()
    user = sp.me()['id']
    pl = sp.user_playlist_create(user, args.playlist, description=args.description)

    # apple_url = 'https://music.apple.com/us/playlist/me-bitch/pl.u-NpXm6X3FmM0lNAV'
    apple_url = input('Enter the URL of the Apple Music Playlist: ')

    soup = BeautifulSoup(requests.get(url=apple_url).content, 'html.parser')

    found = soup.find(id="serialized-server-data")

    df = json.loads(str(found.string)[1:-1]) # Remove leading/trailing brackets
    data = pd.json_normalize(df['data'], max_level=10)
    song_titles = data['sections'][0][1]['items']

    songs = []
    for song in song_titles:
        title = song['title']
        artist = song['subtitleLinks'][0]['title']

        print(f'{title} {artist}')

        songs.append(find_song(title, artist))

        if len(songs) >= 50:
            # Spotify has a 100 song limit per request, so just upload periodically
            sp.playlist_add_items(pl['id'], songs)
            songs = []

    sp.playlist_add_items(pl['id'], songs)


if __name__ == '__main__':
    main()