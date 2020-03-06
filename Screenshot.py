#!usr/bin/env python
import pyautogui
import subprocess
import time
import os
from path import Path
import datetime


def start(name):
    loc_ss = Path()
    if not os.path.exists(loc_ss):
        os.mkdir(loc_ss)
    os.chdir(loc_ss)
    myscreenshot = pyautogui.screenshot()
    myscreenshot.save(name)


def capture_ss():
    try:
        currdt = datetime.datetime.now()
        current_time = currdt.strftime("%H:%M:%S").replace(":", "-")
        filename = 'abc_' + current_time + '.png'
        start(filename)
        time.sleep(5)
        capture_ss()
    except NotImplementedError:
        subprocess.call("sudo apt-get install scrot", shell=True)
        capture_ss()
    except KeyboardInterrupt:
        print()
        exit()


if __name__ == '__main__':
    capture_ss()
