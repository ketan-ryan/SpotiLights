import os
import time
import shutil
import spotipy
import requests
import threading
import spotipy.util as util
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyClientCredentials

with open('secrets.txt', 'r') as fp:
    client_id = fp.readline()
    client_secret = fp.readline()

username = 'kyurembeats2'
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
try:
    token = util.prompt_for_user_token(username,
                                        scope,
                                        client_id,
                                        client_secret,
                                        redirect_uri='http://localhost:8888/callback')
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret),auth=token)

if not token:
    print('Error authenticating user')
current_song = ''

sleeping_time = 0.1
def get_song_info():
    global current_song
    seconds = int(time.time())
    current_song = spotify.current_user_playing_track()['item']['name']

def print_song_info(song):
    global current_song
    if current_song != song:
        print(current_song)

while True:
    get_song_info()
    print_song_info(spotify.current_user_playing_track()['item']['name'])
    timer = threading.Timer(sleeping_time, print_song_info, (current_song,))
    timer.start()

images = spotify.current_user_playing_track()['item']['album']['images']
img_url = images[-1]['url']

r = requests.get(img_url, stream=True)
if r.status_code == 200:
    r.raw.decode_content = True

    with open('img.jpg', 'wb') as fp:
        shutil.copyfileobj(r.raw, fp)

    print('Image successfully downloaded')
else:
    print('Error retrieving image')

