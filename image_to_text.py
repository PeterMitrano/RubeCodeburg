#!/usr/bin/env python3

import argparse
import requests
import sys

def label(url):
    req = {
            "requests": [
                {
                    "image": {
                        "source": {
                            "imageUri": url
                            }
                        },
                    "features": [
                        {
                            "type": "LABEL_DETECTION","maxResults": 5
                            }
                        ]
                    }
                ]
            }

    TOKEN = "ya29.Gl3qBKLsVkzZn1OfVCznNiXnWAJublkQPT5JhJqShxw9tR1a3AlCzeIS39QWK6aZFPK2mzjIb8847b6TmAR5_z4D5AeguDpxvLTdKh0G6s16-pGp-EovBhVDuRYj6lY"
    url = "https://vision.googleapis.com/v1/images:annotate"
    headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + TOKEN}
    r = requests.post(url, json=req, headers=headers)

    if not r.ok:
        return -1, None, r.json()

    label_scores = {}
    for response in r.json()['responses']:
        for label in response['labelAnnotations']:
            label_scores[label['description']] = label['score']

    return 0, label_scores, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', help='url of the image to label')
    args = parser.parse_args()

    code, label_scores, error = label(args.url)

    if code >= 0:
        print(label_scores)
    else:
        print(error)

    return code

if __name__ == '__main__':
    sys.exit(main())
