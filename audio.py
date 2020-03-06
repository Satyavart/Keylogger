
from sys import byteorder
from array import array
from struct import pack
import pyaudio
import time
import wave
import os
from path import Path
import datetime


THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100
sec = 120

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r


def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data


def add_silence(snd_data, seconds):
    silence = [0] * int(seconds * RATE)
    r = array('h', silence)
    r.extend(snd_data)
    r.extend(silence)
    return r


def record():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')
    for i in range(0, int(RATE / CHUNK_SIZE * sec)):
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()
    try:
        r = normalize(r)
        r = trim(r)
    except:
        pass
    r = add_silence(r, 0.5)
    return sample_width, r


def start(filename):
    loc_ss = Path()
    if not os.path.exists(loc_ss):
        os.mkdir(loc_ss)
    os.chdir(loc_ss)
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


def recording():
    try:
        print("please speak a word into the microphone")
        currde = datetime.datetime.now()
        current_time = currde.strftime("%H:%M:%S").replace(":", "-")
        filename = "audio_" + current_time + ".wav"
        start(filename)
        time.sleep(360)
        recording()
    except KeyboardInterrupt:
        print()
        exit()


if __name__ == '__main__':
    recording()
    print("done - result written to demo.wav")

