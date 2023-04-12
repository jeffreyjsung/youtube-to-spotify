import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import yt_dlp


class Playlist(object):
    def __init__(self, playlist_id, title):
        self.id = playlist_id
        self.title = title


class Song(object):
    def __init__(self, track, item_id):
        self.title = track
        self.id = item_id


def extract_artist_and_track_from_video(video_id):
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    video = yt_dlp.YoutubeDL({'quiet': True}).extract_info(
        youtube_url, download=False
    )

    title = video["title"]
    return title


class YouTubeClient(object):
    def __init__(self, client_secrets_file):
        scopes = ["https://www.googleapis.com/auth/youtube"]

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        self.youtube = youtube

    def get_playlists(self):
        request = self.youtube.playlists().list(
            part="id, snippet",
            maxResults=25,
            mine=True
        )

        response = request.execute()

        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]

        return playlists

    def get_videos_from_playlist(self, playlist_id):
        request = self.youtube.playlistItems().list(
            playlistId=playlist_id,
            part="id, snippet"
        )

        response = request.execute()

        songs = []
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            item_id = item['id']
            track = extract_artist_and_track_from_video(video_id)
            if track:
                songs.append(Song(track, item_id))

        return songs

    def remove_videos_from_playlist(self, item_ids):
        for item_id in item_ids:
            request = self.youtube.playlistItems().delete(
                id=item_id
            )
            request.execute()
