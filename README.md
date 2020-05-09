# YoutubeToSpotify
A script to create a Spotify Playlist from a Youtube Playlist (up to 100 songs so far).

## Download
Install all the needed packages

```bash
pip install spotipy
```

```bash
pip install requests
```
```bash
pip install bs4
```

## Get your spotify username
Go to [Account Overview](https://www.spotify.com/us/account/overview/). 

Get your username and replace it in the scrpit (ligne 8). 

## Register your app
Open your [Dashboard](https://developer.spotify.com/dashboard/applications) and create a client ID.

Retrieve your client ID and your client secret and replace them in the scrpit (ligne 16,17).

## Fill the rest of the code 
Paste your Youtube Playlist URL (**MUST BE PUBLIC OR UNLISTED**) in the scrpit (ligne 68). 

Choose your playlist title and descrpition (ligne 71,72). 



## Issues to be fixed
Retrieving more than 100 songs from Youtube. 

