import requests
import json
import spotipy
import spotipy.util as util


def main():
    _url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
    _key = 'a9db524bed3e4c85a9893bfe7321c9aa'

    client_id = "dea84cf8f34e4ddc9cc2d1ca1be98be2"
    client_secret = "79aa711f7bba425889c8a9c99a5e2ab4"
    redirect_uri = "http://localhost"
    scope = 'user-library-read'
    username = '21hq53uurjuec22mf5dbys6li'
    token = util.prompt_for_user_token(
        username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
    tracks_uri = get_tracks_uri_from_playlist(sp)
    valence_list = valence_each_track(tracks_uri,sp)


def get_tracks_uri_from_playlist(sp):
    """ get user playlist tracks"""
    tracks_uri = []
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        tracks_uri.append(track['uri'])
    return tracks_uri

def valence_each_track(tracks_uri,sp):
    """ get the valence for each track"""
    print sp.audio_features(tracks_uri)
    # for track in tracks:


def calculate_distance():
    """ calculate the euclidean distance between each track's valence and the emotion valence """
    pass

def get_top_tracks(n):
    pass

def user_playlist_create(user, name, public=True):
    pass
    # get the top 10 tracks
    # create a new playlist by adding the top 10 tracks


def get_valence_score_from_emotion():
    # 'application/octet-stream',
    emotion_headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': _key,
    }
    with open('waynes.png', 'rb') as f:
        data = f.read()
    req = requests.post(_url, data=data, headers=emotion_headers)
    response_json = req.json()[0]

    # get the most likely emotion
    happy = 0
    sad = 0
    neutral = 0.5
    emotion = ""
    sad_emotions = ["sadness", "contempt", "disgust", "anger", "fear"]
    happy_emotions = ["happiness", "surprise"]
    for key in response_json["scores"]:
        if key in sad_emotions:
            sad += response_json["scores"][key]
        elif key in happy_emotions:
            happy += response_json["scores"][key]
    print happy, sad
    # valence between the range of 0 to 1
    valence_score = neutral + (happy - sad) / 2.0

    return valence_score


if __name__ == '__main__':
    main()
