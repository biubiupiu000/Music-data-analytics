import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json


def getAudioFeatures():
    scope = ""
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    with open('alltracks.json', mode='r', encoding='utf-8') as f:
        tracks = json.load(f)  # load track data
    count = 0
    totalcount = 0
    tracklist = []

    for genre in tracks:
        for artist in tracks[genre]:
            for num, track in enumerate(tracks[genre][artist]):
                if len(track) == 17:  # skip tracks have abnormal attribute number
                    count += 1
                    tracklist.append(track)
                else:
                    del tracks[genre][artist][num]
                    continue
                if count >= 100:  # collect 100 tracks as a batch to reduce API calls
                    ids = [i['id'] for i in tracklist]
                    result = spotify.audio_features(ids)
                    for index, i in enumerate(tracklist):
                        i['audio_features'] = result[index]  # insert new attribute 'audio_features'
                    tracklist = []
                    totalcount += count
                    print(totalcount)
                    count = 0
    if count > 0:  # get last few tracks
        ids = [i['id'] for i in tracklist]
        result = spotify.audio_features(ids)
        for index, i in enumerate(tracklist):
            i['audio_features'] = result[index]
        totalcount += count
        print(totalcount)
    with open('alltracksFeature.json', mode='w', encoding='utf-8') as f:
        json.dump(tracks, f, indent=4, ensure_ascii=False)  # write data to file


if __name__ == '__main__':
    getAudioFeatures()
