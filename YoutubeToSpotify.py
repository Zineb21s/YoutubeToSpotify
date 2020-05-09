import spotipy as spotipy
import spotipy.util as util
from bs4 import BeautifulSoup
import requests
import re

#Spotify username
username = "get_your_username"

scope = 'playlist-modify-public'

# You need to add the redirect uri in your app
redirect = 'http://google.com/'

# Register an app on spotify and get this
client_id = "get_your_client_id"
client_secret = "get_your_secret_id"


def getYTSongs(url):
    # Due to infinite scroll, you can only get 100 songs with bs4, to be fixed.
    sourceCode = requests.get(url).text
    soup = BeautifulSoup(sourceCode, 'html.parser')
    domain = 'https://www.youtube.com'
    songs = []
    for link in soup.find_all("a", {"dir": "ltr"}):
        href = link.get('href')
        if href.startswith('/watch?'):
            # print(link.string.strip())
            youtube_url = domain + href + '\n'
            print(youtube_url)
            songs.append(link.string.strip())
    return songs


def cleanTitle(title):
    title = re.sub(r'\(.*\)', '', title)  # Remove anything within ()
    title = re.sub(r'\[.*\]', '', title)  # Remove anything within []
    title = re.sub(r'\*.*\*', '', title)  # Remove anything within **
    # Remove ft/feat because it's easier to find the correct song on Spotify
    title = title.lower().replace('feat', '')
    title = title.lower().replace('ft', '')
    return title


def findSong(title):
    return sp.search(title, limit=1, type='track', market=None)


def getSongId(song):
    try:
        return song['tracks']['items'][0]['id']
    except:
        return False


def addSong(song, playlist, user):
    sp.user_playlist_add_tracks(user, playlist, [song])


token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret,
                                   redirect_uri=redirect)

if token:
    sp = spotipy.Spotify(auth=token)

    #The youtube playlist must be public 
    url = "Put your playlist url"

    songs = getYTSongs(url)
    title = "Put your Playlist title"
    desc = "Put your description"
    sp.user_playlist_create(username, title, public=True, description=desc)
    playlists = sp.current_user_playlists()
    playlist_Id = playlists['items'][0]['id']
    print(songs)
    for song in songs:
        clean_title = cleanTitle(song)
        music = findSong(clean_title)
        songId = getSongId(music)
        if songId:
            addSong(songId, playlist_Id, username)
            print("yes?")
        else:
            print(song + "not found!")

else:
    print("nopeeee")
