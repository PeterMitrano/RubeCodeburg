
# coding: utf-8

# In[131]:

import cv2
import numpy
import matplotlib.pyplot as plt
from google.cloud import vision
from pygame import mixer
import io
from boto3 import Session

from IPython.display import display,Audio,HTML

# for having playable audio
def show_playable_audio(path):
    html = "<audio controls><source src={} type='audio/mp3'></audio>".format(path)
    display(HTML(html))


# In[116]:

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

plt.imshow(frame)
plt.show()


# In[134]:

client = vision.ImageAnnotatorClient()


# In[121]:

with io.open('./test.jpg', 'rb') as image_file:
        content = image_file.read()
        
image = vision.types.Image(content=content)
#image = vision.types.Image(content=frame.tobytes())


# In[122]:

response = client.text_detection(image=image)
texts = response.text_annotations
# req = {
#     'image': {
#         'content': b64_image
#     },
#     'features': [
#         {
#             'type': vision.enums.Feature.Type.TEXT_DETECTION
#         },
#         {
#             'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION
#         }
#     ]
# }
# response = client.annotate_image(req)


# In[123]:

if len(texts) > 0:
    print(texts[0].description)
    text_to_say = texts[0].description
else:
    print("failure.")
    text_to_say = 'test_text'


# In[78]:

session = Session()
polly = session.client("polly")


# In[125]:

response = polly.describe_voices()
# response


# In[126]:

response = polly.synthesize_speech(Text=text_to_say, VoiceId="Matthew", OutputFormat="mp3")
data = response['AudioStream'].read()


# In[129]:

import copy
data = copy.copy(data)
out_path = "out.mp3"
out_f = open(out_path, 'wb')
out_f.write(data)
out_f.close()


# In[130]:

show_playable_audio(out_path)


# In[132]:

mixer.init()
mixer.music.load(out_path)
mixer.music.play()


# In[ ]:



