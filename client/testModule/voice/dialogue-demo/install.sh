#!/bin/bash

bin_path=$(dirname $(readlink -f $0))

# 話者認識学習音声の録音用
bash ${bin_path}/setup/install4recatr.sh
sudo apt-get install julius -y
sudo apt-get install osspd -y

# 音声認識の julius yomi2voca 用
sudo apt-get install nkf -y

# 話者認識用
bash ${bin_path}/setup/install4htk.sh
sudo apt-get install libsvm-tools -y
sudo apt-get install lib32std++6 -y
sudo apt-get install python-numpy -y
sudo apt-get install python3-numpy -y

# 音声合成
#cd ${bin_path}/setup/source
#bash install4syn.sh
#cd ${bin_path}

sudo apt-get install open-jtalk -y
sudo apt-get install open-jtalk-mecab-naist-jdic -y
sudo apt-get install hts-voice-nitech-jp-atr503-m001 -y
