import datetime
import os
import shutil
import pyaudio
import wave
import requests
import json
import numpy as np
import sys
sys.path.append(os.path.abspath('../..'))
from helperModule import helper

DEVICE_INDEX = 14        # デバイスによって異なるゾ〜
CHUNK = 1024
FORMAT = pyaudio.paInt16 # 16bit
CHANNELS = 1             # monaural
RATE = 44100             # sampling frequency [Hz]

threshold = 0.10         # 音量の閾値

def anyone_speaking():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index = DEVICE_INDEX,
                    frames_per_buffer=CHUNK)
    while True:
        data = stream.read(CHUNK)
        x = np.frombuffer(data, dtype="int16") / 32768.0

        if x.max() > threshold:
            print(x.max())
            return True

def record():
    rec_time = 5 # record time [s]
    # TODO : test. あとで消す。

    now = datetime.datetime.now()
    filename = 'log_' + now.strftime('%Y%m%d_%H%M%S')
    log_path = './log/' + filename + '.wav'

    # TODO : なぜかここで出力される原因の究明
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index = DEVICE_INDEX,
                    frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(log_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return log_path, filename

def get():
    # TODO : URLを指定する。
    url = 'http://demo.ben.hongo.wide.ad.jp:8000/api/message/list'
    module_name = "voice"
    alert = True
    description = "本人ではない人の声を検出しました。"
    content = ""

    helper.send_json(module_name, alert, description, content)

def anomaly_detection():
    if os.path.exists('output'):
        shutil.rmtree('output')
    os.mkdir('log')
    os.mkdir('output')

    # 以下は試験中フェーズ
    while True:
        # TODO : 音量がしきい値を超えたら録音スタート
        if anyone_speaking() == True:
            pass

        # caution : log_pathは相対パス
        # caution : log_filenameは、録音ファイルがAAA.wavならAAA
        log_path, log_filename = record()
        os.system('./dialogue-demo/sid/test.sh ./' + log_path + ' ./output/' + log_filename + '.txt')
        with open('./output/' + log_filename + '.txt') as f:
            s = f.read()
            s = s[0]
            # 暫定でkanayaの声でない場合アラートを出す。
            if s != '1':
                get()
