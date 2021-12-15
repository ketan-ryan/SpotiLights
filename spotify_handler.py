import os
import shutil
import spotipy
import requests
import spotipy.util as util
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyHandler:
    client_id = ''
    client_secret = ''
    spotify = None
    token = None
    username = 'kyurembeats2'
    scope = 'user-read-private user-read-playback-state user-modify-playback-state'
    current_song = ''


    def __init__(self) -> None:
        with open('secrets.txt', 'r') as fp:
            self.client_id = fp.readline().strip()
            self.client_secret = fp.readline().strip()
        try:
            self.token = util.prompt_for_user_token(self.username,
                                                self.scope,
                                                self.client_id,
                                                self.client_secret,
                                                redirect_uri='http://localhost:8888/callback')
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{self.username}")
            self.token = util.prompt_for_user_token(self.username, self.scope)

        if not self.token:
            print('Error authenticating user')

        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(self.client_id, self.client_secret),auth=self.token)
        print('Authenticated successfully')


    def get_song_info(self):
        self.current_song = self.spotify.current_user_playing_track()['item']['name']
        print(f'Current song: {self.current_song}')
        return


    def has_song_changed(self):
        if self.current_song != self.spotify.current_user_playing_track()['item']['name']:
            print(self.current_song)
            return True
        return False


    def get_art(self):
        images = self.spotify.current_user_playing_track()['item']['album']['images']
        img_url = images[-1]['url']

        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True

            with open('img.jpg', 'wb') as fp:
                shutil.copyfileobj(r.raw, fp)

            print('Image successfully downloaded')
        else:
            print('Error retrieving image')
