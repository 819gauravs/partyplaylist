import requests
import json
# sad + contempt + disgust + anger + fear
# neutral
# happy + suprise
def main():
    _url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
    _key = 'a9db524bed3e4c85a9893bfe7321c9aa'
    _maxNumRetries = 10
    #'application/octet-stream',
    headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': _key,
    }
    with open( 'waynes.png', 'rb' ) as f:
        data = f.read()
    req = requests.post(_url,data=data,headers=headers)
    response_json = req.json()[0]

    # get the most likely emotion
    happy = 0
    sad = 0
    neutral = 0.5
    emotion = ""
    sad_emotions = ["sadness","contempt","disgust","anger","fear"]
    happy_emotions = ["happiness", "surprise"]
    for key in response_json["scores"]:
        if key in sad_emotions:
            sad+= response_json["scores"][key]
        elif key in happy_emotions:
            happy+= response_json["scores"][key]
    print happy, sad
    # valence between the range of 0 to 1
    valence_score = neutral + (happy - sad) / 2.0
 


if __name__ == '__main__':
    main()
