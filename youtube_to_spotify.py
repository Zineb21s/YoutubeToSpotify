"""This script is to create a Spotify Playlist from a Youtube Playlist (up to 100 songs so far)."""
import re
import sys
import spotipy
import requests
from spotipy import util
from bs4 import BeautifulSoup
import config


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

if len(sys.argv) > 1:
    USERNAME = sys.argv[1]
else:
    print("Please enter username")
    sys.exit()

token = util.prompt_for_user_token(USERNAME, config.SCOPE, client_id=config.CLIENT_ID,
                                   client_secret=config.CLIENT_SECRET, redirect_uri=config.REDIRECT)

if token:
    sp = spotipy.Spotify(auth=token)

    # The youtube playlist must be public
    URL = "https://www.youtube.com/playlist?list=PL_8qg6E2ChVQyMAn53OQkij73ESJWmRTn"

    songs = get_yt_songs(URL)
    TITLE = " "
    DESC = " "
    sp.user_playlist_create(USERNAME, TITLE, public=True, description=DESC)
    playlists = sp.current_user_playlists()
    playlist_Id = playlists['items'][0]['id']
    for song in songs:
        cleaned_title = clean_title(song)
        if len(cleaned_title) > 0:
            music = find_song(cleaned_title)
            songId = get_song_id(music)
            if songId:
                add_song(songId, playlist_Id, USERNAME)
                # print("yes?")
            else:
                print(song + " not found!")
        else:
            print("The video has been deleted or it is private.")

else:
    print("nopeeee")
