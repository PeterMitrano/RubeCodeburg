#!/usr/bin/env python3
import sys

import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np

from grip import GripPipeline


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

    if args.save:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        print("Saving to file {}".format(args.save))
        out = cv2.VideoWriter(args.save, fourcc, 20.0, (640, 480))

    while True:
        ret, frame = cap.read()

        if ret:
            pipeline.process(frame)

            if len(pipeline.find_blobs_output) > 0:
                frame_with_keypoints = cv2.drawKeypoints(pipeline.hsv_threshold_output, pipeline.find_blobs_output, frame)
                print(pipeline.find_blobs_output)
                cv2.imshow('keypoints', frame_with_keypoints)
                d.append(1)
            else:
                d.append(0)

            if args.verbose:
                cv2.imshow('original', frame)

            if args.save:
                out.write(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    if args.save:
        out.release()
    cv2.destroyAllWindows()

    plt.plot(d)
    # plt.show()


if __name__ == '__main__':
    sys.exit(main())
