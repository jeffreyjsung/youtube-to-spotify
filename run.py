from dotenv import dotenv_values
from spotify import SpotifyClient
from youtube import YouTubeClient

config = dotenv_values(".env")
CLIENT_ID = config['SPOTIFY_CLIENT_ID']
CLIENT_SECRET = config['SPOTIFY_CLIENT_SECRET']
REDIRECT_URI = config['REDIRECT_URI']


def run():
    # 1. Get user's YouTube and Spotify playlists
    youtube_client = YouTubeClient('./creds/client_secret.json')
    playlists = youtube_client.get_playlists()

    spotify_client = SpotifyClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    spotify_playlists = spotify_client.get_playlists()

    # 2. Ask user to choose playlists to transfer to and from
    for i, playlist in enumerate(playlists):
        print(f"{i + 1}: {playlist.title}")

    choice = int(input("Choose a YouTube playlist to transfer from: "))
    chosen_playlist = playlists[choice-1]
    print(f"{chosen_playlist.title} selected.")

    for i in range(len(spotify_playlists) + 1):
        if i == 0:
            print(f"{i}: CREATE A NEW PLAYLIST")
        else:
            print(f"{i}: {spotify_playlists[i - 1].title}")

    spotify_choice = int(input("Choose a Spotify playlist to add the songs to: "))
    if spotify_choice == 0:
        pass
        chosen_spotify_playlist = None
    else:
        chosen_spotify_playlist = spotify_playlists[spotify_choice - 1]
        print(f"{chosen_spotify_playlist.title} selected.")

    # 3. Get songs from YouTube playlist
    songs = youtube_client.get_videos_from_playlist(chosen_playlist.id)
    print(f"Attempting to transfer {len(songs)} tracks...")

    # 4. Search for the songs on Spotify and add them to the chosen playlist
    track_uris = []
    for song in songs:
        track = spotify_client.get_song(song.title)
        if track:
            track_uris.append(track.uri)
    spotify_client.add_songs_to_playlist(track_uris, chosen_spotify_playlist.id)
    print("Success!")

    # 5. Ask if user would like to remove the songs from the YouTube playlist
    remove = int(input("""Would you like to remove the transferred songs from your YouTube playlist?\n
                          0: No\n
                          1: Yes\n
                          Answer: """))
    if remove:
        youtube_client.remove_videos_from_playlist([song.id for song in songs])
        print("Done.")


if __name__ == '__main__':
    run()
