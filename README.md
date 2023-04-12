# YouTube To Spotify
This program will allow you to transfer songs from a YouTube playlist to a Spotify playlist.
## Local Setup
1. Create a project in your Google Developers Console and obtain OAuth 2.0 authorization credentials.
   - Download the `client_secret_XXXXX.json` file, rename it `client_secret.json`, and put it in the `creds` folder.
2. Make sure the YouTube Data API is one of the services that your application is registered to use: 
   - Go to the API Console and select the project that you just registered.
   - Visit the Enabled APIs page. 
   - In the list of APIs, make sure the status is ON for the YouTube Data API v3.
3. Register a Spotify App in your Spotify Developer Dashboard and add https://localhost/ as a Redirect URI in the app settings.
4. Create a `.env` file at the root of the project based on `.env.example` and add your unique `CLIENT_ID` and `CLIENT_SECRET` from the Spotify dashboard.
5. Ensure you have `python3` installed.
6. Run `pip install requirements.txt` (use a virtual environment if you wish).
7. Run `python3 run.py` and follow the instructions.