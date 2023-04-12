import requests
import urllib.parse

from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth


class Playlist(object):
    def __init__(self, playlist_id, title):
        self.id = playlist_id
        self.title = title


class Song(object):
    def __init__(self, id, uri):
        self.id = id
        self.uri = uri


def get_access_token(client_id, client_secret, redirect_uri):
    scope = "playlist-modify-private playlist-modify-public playlist-read-private"
    spotify_oauth = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = spotify_oauth.authorization_url("https://accounts.spotify.com/authorize")
    print('Please go here and authorize: ', authorization_url)

    redirect_response = input('Paste the URL you were redirected to after logging in: ')
    auth = HTTPBasicAuth(client_id, client_secret)

    response = spotify_oauth.fetch_token("https://accounts.spotify.com/api/token", auth=auth,
                                         authorization_response=redirect_response)

    return response["access_token"]


class SpotifyClient(object):
    def __init__(self, client_id, client_secret, redirect_uri):
        self.api_token = get_access_token(client_id, client_secret, redirect_uri)
        self.redirect_uri = redirect_uri

    def get_playlists(self):
        url = "https://api.spotify.com/v1/me/playlists?limit=50"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        response_json = response.json()

        results = response_json['items']
        if results:
            return [Playlist(item['id'], item['name']) for item in results]
        else:
            raise Exception("No playlists found")

    def get_song(self, track):
        query = urllib.parse.quote(track)
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        response_json = response.json()

        results = response_json['tracks']['items']
        if results:
            return Song(results[0]['id'], results[0]['uri'])
        else:
            raise Exception(f"No song found for {artist} - {track}")

    def add_songs_to_playlist(self, song_uris, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            },
            json={
                "uris": song_uris
            }
        )

        return response.ok

    def create_playlist(self, title):
        pass
