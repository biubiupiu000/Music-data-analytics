import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json


def getArtist():
    scope = "user-library-read"
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    genres = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass',
              'blues',
              'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill',
              'classical',
              'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco',
              'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro',
              'french',
              'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy',
              'hard-rock',
              'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian',
              'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop',
              'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno',
              'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop',
              'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b',
              'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad',
              'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul',
              'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance',
              'trip-hop',
              'turkish', 'work-out', 'world-music']
    artists = dict()
    # get artists from all genres
    for genre in genres:
        results = spotify.search(q='genre:' + genre, limit=50, type='artist', offset=0)['artists']
        artists[genre] = results['items']
        while results['offset'] < 950 and results['offset'] + 50 < results['total']:
            results = spotify.next(results)['artists']
            artists[genre].extend(results['items'])
    # save data to file
    with open('artists.json', mode='w', encoding='utf-8') as f:
        json.dump(artists, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    getArtist()
