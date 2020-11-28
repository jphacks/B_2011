import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import os
import subprocess
import shutil
import pyaudio
import wave
import math
import datetime
import time
import torch
import sys
import json
from scipy.fftpack.realtransforms import dct
from sklearn.svm import SVC 

DEVICE_INDEX = 14        # デバイスによって異なるゾ〜
CHUNK = 1024
FORMAT = pyaudio.paInt16 # 16bit
CHANNELS = 1             # monaural
RATE = 44100             # sampling frequency [Hz]

threshold = 0.25         # 音量の閾値
nceps = 12

def anyone_speaking(p, stream):
    while True:
        data = stream.read(CHUNK)
        x = np.frombuffer(data, dtype="int16") / 32768.0

        if x.max() > threshold:
            # print(x.max())
            return

# 波形を適当な長さに分割し、窓関数をかけてFFTを行う。
# start, endは秒数(float ok)
def fft(filename, start, end):
    # 音声の読み込み
    master, fs = sf.read(filename)

    x = master[int(start*fs) : int(end*fs)]
    # ハミング窓をかける
    hamming = np.hamming(len(x))
    x = x * hamming

    # 振幅スペクトルを求める。
    N = 16384 # FFTのサンプル数
    spec = np.abs(np.fft.fft(x, N))[:N//2]
    fscale = np.fft.fftfreq(N, d=1.0/fs)[:N//2]

    return fscale, spec, fs, N


# Hz to mel
def hz2mel(f):
    return 2595 * np.log(f / 700.0 + 1.0)

# mel to Hz
def mel2hz(m):
    return 700 * (np.exp(m / 2595) - 1.0)

# メルフィルタバンクの作成
def melFilterBank(fs, N, numChannels = 20):
    # ナイキスト周波数（Hz）
    fmax = fs / 2
    # ナイキスト周波数（mel）
    melmax = hz2mel(fmax)
    # 周波数インデックスの最大数
    nmax = N // 2
    # 周波数解像度（周波数インデックス1あたりのHz幅）
    df = fs / N
    # メル尺度における各フィルタの中心周波数を求める
    dmel = melmax / (numChannels + 1)
    melcenters = np.arange(1, numChannels + 1) * dmel
    # 各フィルタの中心周波数をHzに変換
    fcenters = mel2hz(melcenters)
    # 各フィルタの中心周波数を周波数インデックスに変換
    indexcenter = np.round(fcenters / df)
    # 各フィルタの開始位置のインデックス
    indexstart = np.hstack(([0], indexcenter[0:numChannels - 1]))
    # 各フィルタの終了位置のインデックス
    indexstop = np.hstack((indexcenter[1:numChannels], [nmax]))
    filterbank = np.zeros((numChannels, nmax))
    for c in range(0, numChannels):
        # 三角フィルタの左の直線の傾きから点を求める
        increment= 1.0 / (indexcenter[c] - indexstart[c])
        for i in range(int(indexstart[c]), int(indexcenter[c])):
            filterbank[c, i] = (i - indexstart[c]) * increment
        # 三角フィルタの右の直線の傾きから点を求める
        decrement = 1.0 / (indexstop[c] - indexcenter[c])
        for i in range(int(indexcenter[c]), int(indexstop[c])):
            filterbank[c, i] = 1.0 - ((i - indexcenter[c]) * decrement)

    return filterbank, fcenters

# 離散コサイン変換を行う。
def disc_cos(mspec):
    ceps = dct(10 * np.log10(mspec), type=2, norm="ortho", axis=-1)
    mfcc = ceps[:nceps]
    return mfcc

def normalization(vague_vowel):
    square_sum = 0
    for i in vague_vowel:
        square_sum += i*i
    norm = math.sqrt(square_sum)
    for i in range(len(vague_vowel)):
        vague_vowel[i] /= norm
    return vague_vowel

def record(p, stream):
    # print('録音開始！')
    rec_time = 5 # [sec]

    now = datetime.datetime.now()
    filename = 'log_' + now.strftime('%Y%m%d_%H%M%S') + '.wav'
    filepath = os.path.join('./log', filename)

    frames = []
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)

    wf = wave.open(filepath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

    return filepath

def svm_model(X_train, Y_train):
    model = SVC(gamma = 'scale')
    model.fit(X_train, Y_train)
    return model

def voice_inference(model, filename):
    dic = {'0':0, '1':0, '2':0, '3':0}
    fig = plt.figure()
    for i in range(5):
        vague_vowel = [0] * nceps
        for j in range(10):
            fscale, spec, fs, N = fft(filename, (i*5+j)*0.1, (i*5+j+1)*0.1)
            filterbank, fcenters = melFilterBank(fs, N, numChannels=20)

            # 振幅スペクトルにメルフィルタバンクを適用
            mspec = np.dot(spec, filterbank.T)
            mfcc = disc_cos(mspec)
            for k in range(nceps):
                vague_vowel[k] += mfcc[k]
        X_test = np.array(normalization(vague_vowel[1:nceps]))
        X_test = X_test.reshape(1,-1)
        plt.scatter(X_test[0][0], X_test[0][1])
        Y_pred = int(model.predict(X_test)[0])
        dic[str(Y_pred)]+=1
    Y_pred = max(dic, key=dic.get)
    fig.savefig("shun.png")

    return str(Y_pred)

def make_training_model_list():
    Y_train = np.array([i//20 for i in range(40)])
    dir_path = './wav'
    model_list = []
    for i in range(1,4): # 何人いるか
        X_train = np.array([])
        Y_train = np.array([x//20 for x in range(40)])
        for l in [0,i]:
            for j in range(5,25):
                vague_vowel = [0] * nceps
                for s in ['a', 'i', 'u', 'e', 'o']: # 一人あたり何個の音声学習データがあるか
                    filename = os.path.join(dir_path, str(l) + '_' + s +'.wav')
                    fscale, spec, fs, N = fft(filename, 0.2*j, 0.2*(j+1))
                    filterbank, fcenters = melFilterBank(fs, N, numChannels=20)
                    # 振幅スペクトルにメルフィルタバンクを適用
                    mspec = np.dot(spec, filterbank.T)
                    mfcc = disc_cos(mspec)
                    for k in range(nceps):
                        vague_vowel[k] += mfcc[k]
                vague_vowel = normalization(vague_vowel[1:nceps])
                X_train = np.append(X_train, vague_vowel)
        X_train = X_train.reshape(-1, nceps-1) # size : (40, 11)
        model = svm_model(X_train, Y_train)
        model_list.append(model)

        fig = plt.figure()
        for k, s in enumerate(['g','y']):
            x = []
            y = []
            for j in range(20):
                x.append(X_train[k*20+j][0])
                y.append(X_train[k*20+j][1])
            plt.scatter(x,y,c=s)
        fig.savefig('ikuno' + str(i) + '.png')
    
    return model_list

def pyannotate(filename, pipeline, model_list):
    # apply diarization pipeline on your audio file
        diarization = pipeline({'audio': filename})

        # dump result to disk using RTTM format
        with open('./wav/log.rttm', 'w') as f:
            diarization.write_rttm(f)
        
        # iterate over speech turns
        sum_time = 0
        member = {} # {speaker : total time}
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            if speaker in member.keys():
                member[speaker] += (turn.end - turn.start)
            else:
                member[speaker] = (turn.end - turn.start)
            # print(f'Speaker "{speaker}" speaks between t={turn.start:.1f}s and t={turn.end:.1f}s.')
        
        # print(member)
        
        speaking_num = 0
        for speaker in member:
            if member[speaker] >= 1:
                speaking_num += 1
        if speaking_num == 0:
            return
        if speaking_num == 1:
            dic = {'0':0, '1':0}
            for model in model_list:
                pred_num = voice_inference(model, filename)
                dic[pred_num] += 1
            if dic['1'] == 0:
                description = 'the examinee is speaking'
                print(json.dumps({ "module" : "voice_recognition", "alert" : 1, "description" : description }))
                sys.stdout.flush()
                # print('[CAUTION] someone is speaking.....')
            else:
                description = 'someone else is speaking'
                print(json.dumps({ "module" : "voice_recognition", "alert" : 1, "description" : description }))
                sys.stdout.flush()
        if speaking_num >= 2:
            description = 'more than 1 person was detected'
            print(json.dumps({ "module" : "voice_recognition", "alert" : 1, "description" : description }))
            sys.stdout.flush()
            # print('[CAUTION] more than 1 person was detected.....')


# main関数のようなもの。
def anomaly_detection():
    description = 'the examinee is speaking'
    print(json.dumps({ "module" : "voice_recognition", "alert" : 1, "description" : description }))
    # TODO : フロントで母音を言うように出してもらって、それを
    # TODO : './wav/examinee_a.wav'のように保存してもらう。
    # 現状、一時的にexaminee_a.wavをmake_wav()で作成する。
    # TODO : make_wav()は後で消す。
    if os.path.exists('log'):
        shutil.rmtree('log')
    os.mkdir('log')

    # ---------------------------------------------------------
    # ここから下は実際に試験中に音声を認識するフェーズに入る。
    
    # TODO : 取得した音声に対して、音声主を予測する。
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input=True,
                    output = True,
                    input_device_index = DEVICE_INDEX,
                    frames_per_buffer = CHUNK,
                    )
    
    # pyannotateのpipelineを作成
    pipeline = torch.hub.load('pyannote/pyannote-audio', 'sad', pipeline=True)

    model_list = make_training_model_list()

    # print('voice model created')
    description = 'more than 1 person was detected'
    print(json.dumps({ "module" : "voice_recognition", "alert" : 1, "description" : description }))
    
    while True:
        anyone_speaking(p, stream) # 話し始めると以下に進む。
        # print('a noise detected.')
        # print(json.dumps({"alert" : 1, "description" : "a noise detected....."}))
        # sys.stdout.flush()


        filename = record(p, stream)
        pyannotate(filename, pipeline, model_list)
        # dic = {'0':0, '1':0}
        # for model in model_list:
        #     pred_num = voice_inference(model, filename)
        #     dic[pred_num] += 1
        # # print(dic['0'], dic['1'])
        # if dic['1'] == 0:
        #     description = 'the examinee is speaking'
        #     print(json.dumps({ "module" : "voice_recognition", "alert" : 1, "description" : description }))
        #     pass
        # else:
        #     # print('pyannotate started...')
            # pyannotate(filename, pipeline)


anomaly_detection()