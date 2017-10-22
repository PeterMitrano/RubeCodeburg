#!/usr/bin/env python3
import matplotlib.pyplot as plt
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        filtered = cv2.inRange(hsv, np.array([0, 0, 240]), np.array([255, 255, 255]))

		mean = np.mean(filtered)

    cv2.imshow('frame', filtered)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
