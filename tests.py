import unittest

import spotify
import youtube
from spotify import SpotifyClient
from dotenv import dotenv_values

config = dotenv_values(".env")
CLIENT_ID = config['SPOTIFY_CLIENT_ID']
CLIENT_SECRET = config['SPOTIFY_CLIENT_SECRET']
REDIRECT_URI = config['REDIRECT_URI']


class SpotifyTest(unittest.TestCase):

    def __init__(self):
        super().__init__()
        self.spotify_client = SpotifyClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    def test_get_song(self):
        result = self.spotify_client.get_song("seven lions - freesol")
        self.assertIsInstance(result, spotify.Song)

    def test_get_playlists(self):
        result = self.spotify_client.get_playlists()
        for item in result:
            self.assertIsInstance(item, spotify.Playlist)


class YoutubeTest(unittest.TestCase):

    def test_extract_song(self):
        result = youtube.extract_artist_and_track_from_video("7-9DJX8NlHU")
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
