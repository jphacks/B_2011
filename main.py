import soundfile as sf
import time
import datetime
import os
import shutil
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

DEVICE_INDEX = 14        # デバイスによって異なるゾ〜
CHUNK = 1024
FORMAT = pyaudio.paInt16 # 16bit
CHANNELS = 1             # monaural
RATE = 44100             # sampling frequency [Hz]

DIST_THRESHOLD = 0.070

# sentenceの内容を./user/sample.wavに保存
def voice_sample_record(sentence):
    print("以下の文章を音読してください。")
    time.sleep(2)
    print(sentence)

    rec_time = 5 # record time [s]     
    output_path = "./log/user_sample.wav"

    # TODO : なぜかここで出力される原因の究明
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index = DEVICE_INDEX,
                    frames_per_buffer=CHUNK)

    print("recording ...")

    frames = []

    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("done.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    time.sleep(2)

def read_wav_file(filename):
    try:
        wr = wave.open(filename, 'r')
    except FileNotFoundError:
        print("[Error 404] No such file or directory" + filename)
        return 0
    data = wr.readframes(wr.getnframes())
    wr.close()
    wavdata = np.frombuffer(data, dtype="int16") / float((2^15))
    return wavdata

def cepstrum(wavdata):
    # TODO : ハミング窓をかける
    # ham = np.hamming(len(wavdata))
    freq = np.fft.fft(wavdata)
    # plt.plot(freq)
    n = len(freq)
    p = [0] * n
    for i in range(n):
        p[i] = freq[i].real ** 2 + freq[i].imag ** 2
        # p[i] /= n
        p[i] = np.log10(p[i])
    
    freq = np.fft.ifft(p)
    # print(len(freq))
    # plt.plot(freq)
    freq_low_pass = freq[100:156]
    # plt.plot(freq_low_pass)
    return freq_low_pass

def test_record():
    rec_time = 5 # record time [s]
    # TODO : test. あとで消す。

    now = datetime.datetime.now()
    output_path = './log/log_' + now.strftime('%Y%m%d_%H%M%S') + '.wav' 

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

    wf = wave.open(output_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    time.sleep(2)
    
    return output_path

def calc_dist(now_data, user_sample):
    if(len(now_data) != len(user_sample)):
        print("something went wrong while recording.")
        return 0
    n = len(now_data) # == len(user_sample)

    # now_data, user_sampleは複素数。
    # TODO : 実数だけで距離を取っていいのかを確認。
    dist = 0
    for i in range(n):
        now_real = now_data[i].real
        sample_real = user_sample[i].real
        dist += (now_real - sample_real) ** 2
    
    return dist

def is_correct_person(dist):
    return dist <= DIST_THRESHOLD

def main():
    shutil.rmtree('log')
    os.mkdir('log')
    # TODO : 読ませる文章の作成
    # TODO : 声が小さい時などの例外処理
    voice_sample_record("こんにちは、今日は良い天気ですね。")
    # voice_sample_record("あいうえおあいうえおあいうえおあいうえお")

    # TODO : 読ませた文章の読み込み
    filepath = "./log/user_sample.wav"
    wav_raw_data = read_wav_file(filepath)
    
    # 100000:100256に意味はない。
    # 配列小さいほうがなんかよさそう。(あんまわからん。) 
    wav_raw_data = wav_raw_data[100000:100256]
    
    user_cep_data = cepstrum(wav_raw_data)
    np.save("./log/user_sample", user_cep_data)
    time.sleep(1)

    # 以下は試験中フェーズ
    while True:
        now_data_path = test_record()
        now_raw_data = read_wav_file(now_data_path)
        now_raw_data = now_raw_data[100000:100256]
        now_cep_data = cepstrum(now_raw_data)
        dist = calc_dist(now_cep_data, user_cep_data)

        ok = is_correct_person(dist)
        if ok == False:
            print('本人ではない人が話している可能性があります。')


if __name__ == '__main__':
    main()