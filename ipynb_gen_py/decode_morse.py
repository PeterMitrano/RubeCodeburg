
# coding: utf-8

# In[13]:

import matplotlib.pyplot as plt
import cv2
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# In[19]:

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        filtered = cv2.inRange(hsv, np.array([0, 0, 240]), np.array([255, 255, 255]))
        

cap.release()


# In[ ]:



