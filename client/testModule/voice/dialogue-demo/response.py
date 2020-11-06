#!/usr/bin/env python3
# coding: utf-8
#
# 応答生成モジュール
# 基本的には
# - 入力と応答の対応リスト(argv[1])
# - 話者認識結果ID (argv[2])
# - 音声認識結果 (argv[3])
# を受け取って応答文および音声を生成する
#
# 前の応答への依存性を持たせたい場合は引数を追加すれば良い
import sys, os

# 音声合成エンジンのpath
#jtalkbin = '/usr/local/open_jtalk-1.07/bin/open_jtalk '
#options = ' -m syn/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /usr/local/open_jtalk-1.07/dic'

jtalkbin = 'open_jtalk '
options = '-m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic'

# 音声合成のコマンドを生成 (open jtalk を 使う場合
def mk_jtalk_command(answer):
    jtalk = 'echo "' + answer + '" | ' + jtalkbin + options + ';'
    play = 'play -q /tmp/dialogue/out.wav; rm /tmp/dialogue/out.wav;'
    return jtalk + play

if __name__ == '__main__':
    # 応答を辞書 reply に登録
    conf = open(sys.argv[1],'r')
    #conf = codecs.open(sys.argv[1],'r','utf8','ignore')
    reply = {}
    for line in conf:
        line = line.rstrip()
        a = line.split();
        reply[a[0]] = a[1]
    conf.close()

    # 話者ID
    sid = int(sys.argv[2])

    # 認識結果
    asrresult = open(sys.argv[3],'r')
    question = asrresult.read().rstrip()
    asrresult.close()

    # 話者ID と認識結果を表示
    print("SPK"+str(sid)+": "+question)

    # 応答リストから対応する応答を出力
    if question in reply:
        answer = str(reply[question])
    else:
        answer = 'もう一度お願いします'
    print("Silly: " + answer)
    os.system(mk_jtalk_command(answer))

