from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
import sys
from spotipy import util, oauth2
import spotipy
import config
import re
from selenium.webdriver.chrome.options import Options
import logging

logger = logging.getLogger(__name__)

def new_get_auth_response(self):
    logger.info('User authentication requires interaction with your '
                'web browser. Once you enter your credentials and '
                'give authorization, you will be redirected to '
                'a url.  Paste that url you were directed to to '
                'complete the authorization.')

    redirect_info = urlparse(self.redirect_uri)
    redirect_host, redirect_port = util.get_host_port(redirect_info.netloc)

    if redirect_port:
        return self._get_auth_response_local_server(redirect_port)
    else:
        logger.warning('Using `%s` as redirect URI without a port. '
                           'Specify a port (e.g. `%s:8080`) to allow '
                           'automatic retrieval of authentication code '
                           'instead of having to copy and paste '
                           'the URL your browser is redirected to.',
                           redirect_host, redirect_host)

def get_yt_songs(baseURL):
    options = Options()
    options.add_argument("window-size=1920x1080")
    options.headless = True
    videos = []
    titles = []
    driver = webdriver.Chrome(ChromeDriverManager().install(), options= options)

    driver.get(baseURL)

    while True:
        scroll_height = 2000
        document_height_before = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script(f"window.scrollTo(0, {document_height_before  + scroll_height});")
        time.sleep(1.5)
        document_height_after = driver.execute_script("return document.documentElement.scrollHeight")
        if document_height_after == document_height_before:
            break

    videos= driver.find_elements_by_xpath('//*[@id="contents"]')


    for i in range(0,len(videos)):
        title = videos[i].find_elements_by_xpath('//*[@id="video-title"]')


    #print(len(title))



    for i in range(0,len(title)):
        titles.append(title[i].text)

    print("Done...")
    driver.quit()
    return titles

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


def youtube_to_spotify(USERNAME, URL):
    try:
        oauth2.get_auth_response = new_get_auth_response
        global sp
        token = util.prompt_for_user_token(USERNAME, config.SCOPE, client_id=config.CLIENT_ID,
                                        client_secret=config.CLIENT_SECRET, redirect_uri=config.REDIRECT)

        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False

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
                    else:
                        print(song + " not found!")
                else:
                    print("The video has been deleted or it is private.")

        else:
            print("nopeeee")
    except spotipy.SpotifyException:
        print("Spotipy exception")

youtube_to_spotify(	"username", "playlist_url")