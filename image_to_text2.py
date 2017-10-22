#! /usr/bin/env python3
from google.cloud import vision
import opencv

cam = opencv.WebCam(0)
frame = cam.read()


client = vision.imageannotatorclient()
req = {
        'image': {
            'source': {
                'image_uri': ''
                }
            },
        'features': [
            {
                'type': vision.enums.feature.type.face_detection
            }
        ]
    }
response = client.annotate_image(req)

print(response)
#for annotation in response:
    #print(annotation.text_annotations)
