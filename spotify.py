import requests
import urllib.parse


class SpotifyClient(object):
    def __init__(self, api_token):
        self.api_token = api_token

    def get_playlists(self):
        url = "https://api.spotify.com/v1/me/shows?limit=50"
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
            return [item['id'] for item in results]
        else:
            raise Exception("No playlists found")

    def get_song(self, artist, track):
        query = urllib.parse.quote(f'{artist} {track}')
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
            return results[0]['id']
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
