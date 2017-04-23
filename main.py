import requests
import json
import spotipy
import spotipy.util as util
import math
import operator
import config
def main():
    playlist_name = "Will squared Playlist"
    image_file_name = "will&will.jpg"
    maximum = 20
    token = util.prompt_for_user_token(
        config.username, config.scope, client_id=config.client_id, client_secret=config.client_secret, redirect_uri=config.redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)

    if(not duplicates(playlist_name,sp)):
        print "creating new playlist:",playlist_name
        playlist_id = sp.user_playlist_create(config.username,playlist_name,public=True)['id']
    else:
        playlist_id = find_playlist_id(playlist_name,sp)

    # print playlist_id
    tracks_uri = get_tracks_uri_from_playlist(sp)
    tracks_valence = []
    track_dict = {}
    emot_valence = get_valence_score_from_emotion(config._url,config._key,image_file_name)
    for uri in get_tracks_uri_from_playlist(sp):
        # track_dict[uri] = valence_each_track(uri,sp)
        track_dict[uri] = calculate_distance(valence_each_track(uri,sp),emot_valence )
        tracks_valence.append(valence_each_track(uri,sp))
    track_dict_sorted = sorted(track_dict.items(), key=operator.itemgetter(1))
    # print track_dict
    # print tracks_valence
    # print calculate_distance(tracks_valence, get_valence_score_from_emotion(_url,_key))
    # print track_dict_sorted
    # print emot_valence

    uris = []
    for uri in track_dict_sorted[:maximum]:
         uris.append(uri[0])
        # uris.append(uri[0])
    sp.user_playlist_add_tracks(config.username, playlist_id, uris)
    print "done"
    # ensure a duplicate playlist is not created
def find_playlist_id(playlist_name,sp):
    for item in sp.current_user_playlists(limit=50, offset=0)['items']:
        if item['name'] == playlist_name:
            return item['id']

def duplicates(name,sp):
    for item in sp.current_user_playlists(limit=50, offset=0)['items']:
        if item['name'] == name:
            return True
    return False


def get_tracks_uri_from_playlist(sp):
    """ get user playlist tracks"""
    results = sp.current_user_saved_tracks(limit=50)
    for item in results['items']:
        track = item['track']
        yield track['uri']

def valence_each_track(track_uri,sp):
    """ get the valence for each track"""
    tracks_valence = sp.audio_features([track_uri])
    return tracks_valence[0]['valence']

def calculate_distance(tracks_valence,emotion_valence):
    """ calculate the euclidean distance between each track's valence and the emotion valence """
    return abs(tracks_valence - emotion_valence)

def get_valence_score_from_emotion(_url,_key,image_file_name):
    # 'application/octet-stream',
    emotion_headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': _key,
    }
    with open(image_file_name, 'rb') as f:
        data = f.read()
    req = requests.post(_url, data=data, headers=emotion_headers)
    response_json = req.json()
    print req.text
    # get the most likely emotion
    happy = 0
    sad = 0
    neutral = 0.5
    emotion = ""
    sad_emotions = ["sadness", "contempt", "disgust", "anger", "fear"]
    happy_emotions = ["happiness", "surprise"]
    for person in response_json:
        for key in person["scores"]:
            if key in sad_emotions:
                sad += person["scores"][key]
            elif key in happy_emotions:
                happy += person["scores"][key]
    # print happy, sad
    # valence between the range of 0 to 1
    valence_score = neutral + (happy - sad) / (2.0 * len(response_json))
    return valence_score


if __name__ == '__main__':
    main()
