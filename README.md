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

Get your username and replace it in the scrpit (ligne 9). 

## Register your app
Open your [Dashboard](https://developer.spotify.com/dashboard/applications) and create a client ID.

Retrieve your client ID and your client secret and replace them in the scrpit (ligne 17,18).

## Set redirect URIS
Open your [Dashboard](https://developer.spotify.com/dashboard/applications) 

Go to your application.

Click on settings.

Add this as your redirect URI : http://google.com/ 


## Fill the rest of the code 
Paste your Youtube Playlist URL (**MUST BE PUBLIC OR UNLISTED**) in the scrpit (ligne 68). 

Choose your playlist title and descrpition (ligne 77,78). 

## Running the code

You will be required to paste the redirected URI, copy the url of the page you will redirected to (normally google) and paste it in your console. 


## Issues to be fixed
Retrieving more than 100 songs from Youtube. 

