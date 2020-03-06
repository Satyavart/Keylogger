#!usr/bin/env python
import time
import cv2
import os
from path import Path
import datetime


def start(name):
    loc_ss = Path()
    if not os.path.exists(loc_ss):
        os.mkdir(loc_ss)
    os.chdir(loc_ss)
    camera = cv2.VideoCapture(0)
    time.sleep(0.1)
    return_value, image = camera.read()
    cv2.imwrite(name, image)
    del(camera)


def capture_photo():
    try:
        currdt = datetime.datetime.now()
        current_time = currdt.strftime("%H:%M:%S").replace(":", "-")
        filename = 'xyz_' + current_time + '.png'
        start(filename)
        time.sleep(5)
        capture_photo()
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    capture_photo()