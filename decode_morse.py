#!/usr/bin/env python3
import sys

import argparse
import funfax
import cv2
import matplotlib.pyplot as plt
import numpy as np
from time import sleep

from grip import GripPipeline


def from_morse(morse):
    return "hello, world"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action="store_true", help="show windows with input and outputs")
    parser.add_argument('--save', '-s', help="write to output.avi")
    parser.add_argument('--vid', help="input video for testing")

    args = parser.parse_args()

    pipeline = GripPipeline()

    if args.vid:
        cap = cv2.VideoCapture(args.vid)
    else:
        cap = cv2.VideoCapture(0)

    d = []
    fps = 30
    on_frames = 0
    off_frames = 0
    really_off_frames = 0
    on_thresh = fps * 0.05
    dot_thresh = fps * 0.100
    dash_thresh = fps * 0.400
    space_thresh = fps * 0.900
    char_gap_thresh = fps * 0.100
    char_done = False
    dot_done = False
    dash_done = False
    space_done = False
    morse = ""

    if args.save:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        print("Saving to file {}".format(args.save))
        out = cv2.VideoWriter(args.save, fourcc, fps, (640, 480))

    while True:
        ret, frame = cap.read()

        if ret:
            if args.verbose:
                cv2.imshow('original', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            pipeline.process(frame)
            if len(pipeline.find_blobs_output) > 0:
                print("blob")
                w = 20
                kp = pipeline.find_blobs_output[0]
                if w < kp.pt[0] < 480 - w and w < kp.pt[1] < 640 - w:
                    d.append(1)
                    on_frames += 1
            else:
                off_frames += 1
                if off_frames > char_gap_thresh:
                    really_off_frames = off_frames
                    on_frames = 0

                if really_off_frames > char_gap_thresh:
                    if on_frames > dash_thresh:
                        morse += "-"
                        print("-")
                    elif on_frames > dot_thresh:
                        morse += "."
                        print(".")
                d.append(0)

            if args.save:
                out.write(frame)
        else:
            break

    cap.release()
    if args.save:
        out.release()
    cv2.destroyAllWindows()

    print(morse)
    plt.plot(d)
    plt.show()

    text = from_morse(morse)
    # funfax.funfax(text)


if __name__ == '__main__':
    sys.exit(main())
