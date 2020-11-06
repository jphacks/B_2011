#! /bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $ $0 wav-dir output-file"
    exit 1;
fi

wavdir=$1
output=$2


echo -n > $output
for file in `find $wavdir -name '*.wav' | sort`; do
    path=`readlink -f $file`
    spkid=`echo $(basename $path) | sed -e 's/^s\([0-9]\)_b[0-9]\+.wav$/\1/'`
    echo -e "${path}\t${spkid}" >> $output
done

