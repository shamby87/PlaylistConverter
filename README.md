# PlaylistConverter

This tool converts an Apple Music playlist to a Spotify playlist. It needs a link to the Apple Music playlist and authorization to a Spotify account.

## Prerequisits

You will need Python > 3.6 and all the modules used in `convert.py`

You will need to create an app on the Spotify developer dashboard. See the [Spotify](https://developer.spotify.com/documentation/web-api/tutorials/getting-started) page to get started with creating the app and gathering credentials. For the `redirect URI`, use something like `http://localhost:3000`, this server will start automatically for you.

You will use the credentials from the Spotify app you just created to fill out the `.env` file. You will copy the client ID, client secret, and redirect URI to the corresponding fields in `.env`

## Running

`py convert.py [-h] -p PLAYLIST [-d DESCRIPTION] [-u URL]`

The only required argument is `-p PLAYLIST`, where `PLAYLIST` is the name of the playlist you want created on Spotify. When you run this for the first time, a browser window will popup to ask for permission to your Spotify account. Accept this and the window will automatically close. 

If the `URL` argument is left blank, the program will ask for this value to be input in the terminal. This is the URL to the Apple Music playlist you want to be copied to Spotify (e.g. `https://music.apple.com/us/playlist/<PLAYLIST_NAME>/<UNIQUE_ID>`)
