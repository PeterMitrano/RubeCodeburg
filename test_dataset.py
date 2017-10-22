import argparse
import sys

import numpy as np
import cv2
import grip

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--npz", required=True, help="input dataset (*.npz)")
    args = parser.parse_args()

    dataset = np.load(args.npz)
    frames = dataset['frames']
    labels = dataset['labels']

    correct = 0
    for frame, label in zip(dataset['frames'], dataset['labels']):
        pipeline = grip.GripPipeline()
        pipeline.process(frame)

        cv2.imshow('', pipeline.blur_output)
        cv2.waitKey(1)

        blobs = pipeline.find_blobs_output

        if len(blobs) > 0:
            prediction = [1, 0]
        else:
            prediction = [0, 1]

        if np.allclose(prediction, label):
            correct += 1

    accuracy = correct / dataset['labels'].shape[0]
    print("Accuracy: {}".format(accuracy))


if __name__ == '__main__':
    sys.exit(main())
