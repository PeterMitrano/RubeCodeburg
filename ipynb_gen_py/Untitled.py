
# coding: utf-8

# In[3]:

import cv2
import numpy
import matplotlib.pyplot as plt
from google.cloud import vision


# In[6]:

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()


# In[17]:

client = vision.ImageAnnotatorClient()
req = {
    'image': {
        'content': frame
    },
    'features': [
        {
            'type': vision.enums.TextAnnotation
        }
    ]
}
print(vision.annotations.TextAnnotation.)
response = client.annotate_image(req)


# In[ ]:



