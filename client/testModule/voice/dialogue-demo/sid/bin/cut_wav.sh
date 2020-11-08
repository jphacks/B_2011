#! /bin/bash

# wav ファイルを $cutlength [s] ずつカットする（後ろの余りは捨てる）

if [ $# -ne 3 ]; then
    echo "$ bash $0 [wav-spk list] [cutwav-spk list (output)] [cutwav outputdir]"
    exit 1
fi

wavspklist=$1
cutwavspklist=$2
rm -f $cutwavspklist
outputdir=$3
mkdir -p $outputdir
cutlength=1.5


cat $wavspklist | while read line; do
    wavfile=$(echo -e "$line" | cut -f 1)
    if [ ! -s $wavfile ]; then
	echo "Error: $wavfile does not exist!"
	exit 1
    fi

    spkidx=$(echo -e "$line" | cut -f 2)
    wavdir=$(dirname $wavfile)
    wavname=$(basename $wavfile .wav)
    wavlength=$(soxi $wavfile | grep '^Duration' | cut -d ':' -f 4 | cut -d ' ' -f 1)
    cutnum=$(echo "$wavlength / $cutlength" | bc)

    # $cutlength [s] 以下のファイルはカットしない
    if [ $cutnum -eq 0 ]; then
	echo "Not cut $wavfile"
	echo -e "${wavfile}\t$spkidx" >> $cutwavspklist
    else
	for idx in $(seq 1 $cutnum); do
	    cutstart=$(echo "$cutlength * ($idx - 1)" | bc)
	    cutwavfile=${outputdir}/${wavname}_$(printf %02d ${idx}).wav
	    echo "Cut $wavfile ($cutstart : $(echo "$cutstart + $cutlength" | bc))"
	    echo -e "${cutwavfile}\t$spkidx" >> $cutwavspklist
	    sox $wavfile $cutwavfile trim $cutstart $cutlength
	done
    fi
done
