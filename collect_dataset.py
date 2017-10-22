#!/usr/bin/env python3

import argparse
import numpy as np
import cv2
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outfile", "-o", help="output file (*.npz)", required=True)
    args = parser.parse_args()

    n = 2000
    IMG_W = 96
    IMG_H = 72
    frames = np.ndarray(shape=(n, IMG_H, IMG_W, 3), dtype=np.uint8)
    labels = np.ndarray(shape=(n, 2), dtype=np.uint8)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("tmp.avi", fourcc, 30.0, (IMG_W, IMG_H))

    cap = cv2.VideoCapture(0)
    i = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            print("frame error!")
            return 1

        label = [0, 1]
        frame_scaled = cv2.resize(frame, (IMG_W, IMG_H))

        out.write(frame_scaled)
        frames[i] = frame_scaled
        labels[i] = label

        cv2.imshow("scaled", frame_scaled)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        i += 1
        if i > n/2:
            break

    input("Turn on the flash and press enter.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("frame error!")
            return 1

        label = [1, 0]
        out.write(frame_scaled)
        frame_scaled = cv2.resize(frame, (IMG_W, IMG_H))
        cv2.imshow("scaled", frame_scaled)
        frames[i] = frame_scaled
        labels[i] = label

        cv2.imshow("scaled", frame_scaled)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        i += 1
        if i >= n:
            break

    cap.release()

    print(frames[0])
    np.savez(open(args.outfile, 'wb'), frames=frames, labels=labels)


if __name__ == '__main__':
    sys.exit(main())
