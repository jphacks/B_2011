#!/bin/bash
#
# 話者識別精度の算出
#

if [ $# -ne 1 ]; then
    echo "Usage: $ $0 wav-directory"
    exit 1;
fi

## dialogue directory ##
#wavdirname=./record_ATR/wav
wavdirname=`readlink -f $1`
if [ ! -e $1 ]; then
    echo "there are no directory"
    exit 1
fi

# 計算用の中間ファイル
wavlist=$(find $wavdirname -name "*.wav")
sidfile=spkid.txt
sidlist=spkidlist.txt
rm $sidfile $sidlist -f

# 話者認識
for wavfile in $wavlist; do
    bash test.sh $wavfile $sidfile
    echo -n `basename $wavfile` >> $sidlist
    echo -e ":$(cat $sidfile)" >> $sidlist
done

# 正答率の計算
i=0
for line in $(cat $sidlist); do
    ref=$(echo $line | sed -e "s/s\([0-9]\)_b[0-9]*.wav:\([0-9]\)/\1/g")
    ans=$(echo $line | sed -e "s/.*:\([0-9]\)$/\1/g")
    if [ $ref = $ans ]; then
        i=$(( i + 1 ))
    fi
done
datanum=$(wc $sidlist -l | cut -d " " -f 1)
echo -e "accurate prediction:\t$i"
echo -e "data size:\t\t$datanum"
echo -e "prediction accuracy:\t$(expr 100 \* $i / $datanum )%"

# 事後処理
#rm $sidfile $sidfilelist
