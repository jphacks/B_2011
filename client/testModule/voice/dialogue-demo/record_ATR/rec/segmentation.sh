#!/bin/bash
# Segmenatation using "segment.pl"
#
#

# awk, perl, and wc
AWK=gawk;
PERL=/usr/bin/perl;
WC=/usr/bin/wc;

# SPTK bin
X2X=/usr/local/SPTK-3.6/bin/x2x;
FRAME=/usr/local/SPTK-3.6/bin/frame;
WINDOW=/usr/local/SPTK-3.6/bin/window;
MCEP=/usr/local/SPTK-3.6/bin/mcep;
DMP=/usr/local/SPTK-3.6/bin/dmp;

# CHECK ARGUMENTS
num=50

# CHECK THE NUMBER OF SPEECH FILES
fnum=$(ls /work/ssuzuki/lab_seminar/HTS-demo_UT-ISTC50-SPK_2014/data/wav | $WC -l)

pwddir=`pwd`
if [ "/work/ssuzuki/lab_seminar/HTS-demo_UT-ISTC50-SPK_2014/rec" != $pwddir ];then
	echo "You should execute this script at /work/ssuzuki/lab_seminar/HTS-demo_UT-ISTC50-SPK_2014/rec"
	exit 1
fi

if [ $fnum -ne $num ];then
	echo "The # of files is $fnum / $num";
	echo "Please record!!"
	exit 1
fi

# segmentation #
for file in ../data/wav/* ; do
	outname1=../data/labels/mono/$(basename $file .wav).tmp
	outname2=../data/labels/mono/utokyo_jp_istc50_spk_$(basename $file .wav).lab
	labname=reference/monophone/$(basename $file .wav).lab
	/usr/bin/perl segment.pl $file $labname $outname1 
	
	# post processing
	vecnum=$( $X2X +sf $file | $FRAME  -l 400 -p 80 | $WINDOW -l 400 -L 512 -w 1 | $MCEP -a 0.42 -m 12 -l 512 | $DMP +f | $WC -l );
        samplenum=$(( vecnum / 13 ))	
 	samplelen=$(( samplenum * 50000)) ; 
	linenum=$(cat $outname1 | $WC -l);
	head -n $(( linenum - 1 )) $outname1 > $outname2
	( echo -n "$samplelen " ; tail -n 1 $outname1 ) | gawk '{print $2,$1,$4}' >> $outname2 ;
	rm -f $outname1 ;
	rawname=/work/ssuzuki/lab_seminar/HTS-demo_UT-ISTC50-SPK_2014/data/raw/utokyo_jp_istc50_spk_$(basename $file .wav).raw
	/usr/bin/sox $file $rawname
	echo "$file done.";
done
# remove tmp directory
rm -rf /work/ssuzuki/lab_seminar/HTS-demo_UT-ISTC50-SPK_2014/rec/tmp
