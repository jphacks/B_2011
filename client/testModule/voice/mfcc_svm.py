import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import os
from scipy.fftpack.realtransforms import dct
from sklearn.svm import SVC

# 波形を適当な長さに分割し、窓関数をかけてFFTを行う。
def fft(filename):
    # 音声の読み込み
    master, fs = sf.read(filename)

    t = np.arange(0, len(master) / fs, 1/fs)

    # 音声波形の中心部分（定常部）を切り出す
    center = len(master)//2 #　中心のサンプル番号
    cuttime = 0.04 # 秒
    x = master[int(center - cuttime / 2 * fs):int(center + cuttime / 2 * fs)]
    time = t[int(center - cuttime/2*fs): int(center + cuttime/2*fs)]

    #plt.plot(time * 1000, x)
    #plt.xlabel("time [ms]")
    #plt.ylabel("amplitude")
    #plt.show()

    # ハミング窓をかける
    hamming = np.hamming(len(x))
    x = x * hamming

    # 振幅スペクトルを求める。
    N = 2048 # FFTのサンプル数
    spec = np.abs(np.fft.fft(x, N))[:N//2]
    fscale = np.fft.fftfreq(N, d=1.0/fs)[:N//2]

    #plt.plot(fscale, spec)
    #plt.xlabel("frequency [Hz]")
    #plt.ylabel("amplitude spectrum")
    #plt.show()

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
    # print(indexstop)
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
    nceps = 12
    mfcc = ceps[:nceps]
    return mfcc

# TODO : レコードと、クライアント側で出す文字について考える。
def record():
    pass

# TODO : サポートベクターマシンでmfccの分類のためのモデル構築を行う。
def svm_model(X_train, Y_train):
    model = SVC(gamma = 'scale')
    model.fit(X_train, Y_train)
    return model



# main関数のようなもの。
def run():
    dir_path = './dialogue-demo/record_ATR/wav'
    X_train = np.array([])
    Y_train = []
    for i in range(4):
        for j in range(29):
            Y_train.append(i)
    # 学習データの生成
    for i in range(4):
        for j in range(29):
            filename = os.path.join(dir_path, 's' + str(i + 1) +'_b' + str(j+1).zfill(2) +'.wav')
            fscale, spec, fs, N = fft(filename)
            filterbank, fcenters = melFilterBank(fs, N, numChannels=20)

            # 振幅スペクトルにメルフィルタバンクを適用
            mspec = np.dot(spec, filterbank.T)
            mfcc = disc_cos(mspec)
            X_train = np.append(X_train, mfcc)
    X_train = X_train.reshape(-1, 12)
    # print(X_train)

    print('training data created.')
    # TODO : 0-indexに本人の音声のケプストラムを入れたい。
    model = svm_model(X_train, Y_train)
    print('model created.')

    # ---------------------------------------------------------
    # ここから下は実際に試験中に音声を認識するフェーズに入る。
    
    # TODO : 取得した音声に対して、音声主を予測する。
    cnt = 0
    for i in range(4):
        for j in range(30,31):
            filename = os.path.join(dir_path, 's' + str(i+1) +'_b' + str(j).zfill(2) +'.wav')
            fscale, spec, fs, N = fft(filename)
            filterbank, fcenters = melFilterBank(fs, N, numChannels=20)

            # 振幅スペクトルにメルフィルタバンクを適用
            mspec = np.dot(spec, filterbank.T)
            mfcc = disc_cos(mspec)
            X_test = mfcc
            X_test = X_test.reshape(1,-1)
            # print('X_test')
            # print(X_test)
            Y_pred = model.predict(X_test)
            print('answer : ' + str(i) + ' predict : ' + str(Y_pred[0]))
            if i-1==Y_pred[0]:
                cnt+=1
    # Y_pred = model.predict(X_test)
    # print(Y_pred)
    print(cnt)
    print(cnt / 120)

run()