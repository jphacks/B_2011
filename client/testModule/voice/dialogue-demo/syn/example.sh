#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $ $0 [input text]"
    exit 1
fi

inputtext=$1

cat $inputtext | open_jtalk -m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow test.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic 

play -q test.wav
rm -f test.wav
