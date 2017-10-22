#!/usr/bin/env python3
import matplotlib.pyplot as plt
import cv2
import numpy as np
import sys


def main():
    cap = cv2.VideoCapture(0)
    means = []

    while True:
        ret, frame = cap.read()

        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            channels = cv2.split(hsv)
            filtered = cv2.inRange(channels[2], 240, 255)

            mean = np.mean(filtered)
            means.append(mean)

            # Set up the detector with default parameters.
            detector = cv2.SimpleBlobDetector()

            # Detect blobs.
            keypoints = detector.detect(cv2.ORB, image=filtered)

            # Draw detected blobs as red circles.
            # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
            im_with_keypoints = cv2.drawKeypoints(filtered, keypoints, np.array([]), (0, 0, 255),
                                                  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            cv2.imshow('frame', im_with_keypoints)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(1) & 0xFF == ord('s'):
                means.clear()

    cap.release()
    cv2.destroyAllWindows()

    plt.plot(means)
    plt.title("mean brightness")
    plt.show()


if __name__ == '__main__':
    sys.exit(main())
