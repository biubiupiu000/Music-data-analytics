import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

def getTracks():
    scope = ""
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    with open('artists.json', encoding='utf-8') as f:
        artists = json.load(f)  # load artists
    print(len(artists))
    albums = dict()
    startFlag = True  # edit this to False after the first run
    startName = ''  # edit this string to the last artist name output on the last run
    with open('tracks.json', mode='a', encoding='utf-8') as f:  # edit the file name to a different one on each run
        for genre in artists:
            albums[genre] = dict()
            for artistInfo in artists[genre]:
                if not startFlag:  # try to continue from where we left from last run
                    if artistInfo['name'] == startName:
                        startFlag = True
                        continue
                else:
                    try:
                        results = spotify.artist_top_tracks(artistInfo['id'])
                    except:
                        pass
                    albums[genre][artistInfo['name']] = results['tracks']
                    print(artistInfo['name'])
        json.dump(albums, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    import sys
    if not sys.gettrace():
        sys.stderr.write('This script has to be executed in debug mode, please refer to readme for more information.', )
    else:
        getTracks()
