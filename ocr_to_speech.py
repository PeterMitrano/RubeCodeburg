#!/usr/bin/env python3

import argparse
import io
from time import sleep

import cv2
from boto3 import Session
from google.cloud import vision
from pygame import mixer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", '-d', action="store_true", help='cheat for the demo')
    parser.add_argument("--save", '-s', help='cheat for the demo')

    args = parser.parse_args()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if ret:
            cv2.imshow('input', frame)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break

    cap.release()

    if args.save:
        cv2.imwrite(args.save, frame)
        return

    client = vision.ImageAnnotatorClient()

    if args.demo:
        demo_img = "ocr.jpg"
        with io.open(demo_img, 'rb') as image_file:
            image = image_file.read()
    else:
        saved_frame_path = "/tmp/frame.jpg"
        cv2.imwrite(saved_frame_path, frame)
        image = io.open(saved_frame_path, 'rb').read()

    image = vision.types.Image(content=image)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if len(texts) > 0:
        print(texts[0].description)
        text_to_say = texts[0].description
    else:
        print("failure.")
        text_to_say = 'test_text'
        return

    session = Session()
    polly = session.client("polly")

    response = polly.synthesize_speech(Text=text_to_say, VoiceId="Matthew", OutputFormat="mp3")
    data = response['AudioStream'].read()

    out_path = "out.mp3"
    out_f = open(out_path, 'wb')
    out_f.write(data)
    out_f.close()

    print("wrote to file", out_path)

    mixer.init()
    mixer.music.load(out_path)
    mixer.music.play()
    sleep(5)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
