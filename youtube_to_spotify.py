"""This script is to create a Spotify Playlist from a Youtube Playlist (up to 100 songs so far)."""
import re
import requests
import spotipy
import spotipy.util as util
from bs4 import BeautifulSoup

# Spotify username
USERNAME = " "

SCOPE = 'playlist-modify-public'

# You need to add the redirect uri in your app
REDIRECT = 'http://google.com/'

# Register an app on spotify and get this
CLIENT_ID = " "
CLIENT_SECRET = " "


def get_yt_songs(url):
    """Returns all the titles from the Youtube Playlist's videos"""
    # Due to infinite scroll, you can only get 100 songs with bs4, to be fixed.
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'html.parser')
    domain = 'https://www.youtube.com'
    song_titles = []
    for link in soup.find_all("a", {"dir": "ltr"}):
        href = link.get('href')
        if href.startswith('/watch?'):
            # print(link.string.strip())
            youtube_url = domain + href + '\n'
            print(youtube_url)
            song_titles.append(link.string.strip())
    return song_titles


def clean_title(title):
    """Removes anything within (), [], ** and ft/feat in order to
     make it easier to find the correct song on Spotify"""
    title = re.sub(r'\(.*\)', '', title)
    title = re.sub(r'\[.*\]', '', title)
    title = re.sub(r'\*.*\*', '', title)
    title = title.lower().replace('feat', '')
    title = title.lower().replace('ft', '')
    return title


def find_song(title):
    """Returns the song."""
    return sp.search(title, limit=1, type='track', market=None)


def get_song_id(track):
    """Returns the song id if found."""
    try:
        return track['tracks']['items'][0]['id']
    except:
        return False


def add_song(track, playlist, user):
    """Adds the song to the Spotify Playlist."""
    sp.user_playlist_add_tracks(user, playlist, [track])


toke = util.prompt_for_user_token(USERNAME, SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                  redirect_uri=REDIRECT)

if toke:
    sp = spotipy.Spotify(auth=toke)

    # The youtube playlist must be public
    URL = " "

    songs = get_yt_songs(URL)
    TITLE = " "
    DESC = " "
    sp.user_playlist_create(USERNAME, TITLE, public=True, description=DESC)
    playlists = sp.current_user_playlists()
    playlist_Id = playlists['items'][0]['id']
    print(songs)
    for song in songs:
        cleaned_title = clean_title(song)
        music = find_song(cleaned_title)
        songId = get_song_id(music)
        if songId:
            add_song(songId, playlist_Id, USERNAME)
            print("yes?")
        else:
            print(song + "not found!")

else:
    print("nopeeee")
