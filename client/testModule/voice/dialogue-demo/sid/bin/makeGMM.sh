#! /bin/bash

bin_path=$(dirname $(readlink -f $0))
HERestbin=${bin_path}/../../bin/HERest

##############################
# UBMから1発話に適応したGMMを作る #
##############################

# 指定した UBM を初期モデルとして、指定した1発話（mfcc）を MAP 適応して adapted GMM を推定する。
# UBM の混合数と tau（MAP 適応の重み。小さいほど adapted GMM の UBM からの変化が大きくなる）も指定する。

if [ $# -ne 2 ]; then
    echo "Usage: $ bash $0 (mfcc file) (UBM file)"
    exit 1;
fi

mixture=128  # 8, 16, 32, 64
mfccfile=$1  # mfcc
HCompVConf=${bin_path}/../config/config_adapt.train  # HERest の config
UBM=$2  # UBM
GMMdir=${bin_path}/../GMM
mkdir -p $GMMdir
#mkdir -p log

# 学習
weightfloor=1 # 1* 1.0e-5
vfloor=1e-6

segid=$(basename $mfccfile .mfcc)

mkdir -p $GMMdir

$HERestbin -T 1 -C $HCompVConf -u mvp -w $weightfloor -v $vfloor -H $UBM -I ${bin_path}/../jmodel.mlf -M $GMMdir ${bin_path}/../list/modelname $mfccfile

mv $GMMdir/jmodel $GMMdir/$segid
