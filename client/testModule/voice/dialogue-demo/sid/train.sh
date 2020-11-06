#! /bin/bash

bin_path=$(dirname $(readlink -f $0))
HCopybin=${bin_path}/../bin/HCopy
svmscalebin=svm-scale
svmtrainbin=svm-train

if [ $# -ne 1 ]; then
    echo "Usage: $ bash $0 [wav-spk list]"
    exit 1
fi


# 話者識別用 SVM モデルを学習する (GMM supervector ver.)

wavspklist=$1  # (col1: wav)\t(col2: speaker ID) のリスト
cut_wavbin=${bin_path}/bin/cut_wav.sh
HCopyConf=${bin_path}/config/config.HCopy
global_cmn=${bin_path}/bin/global_cmn.py
makeGMMbin=${bin_path}/bin/makeGMM.sh
extractSVbin=${bin_path}/bin/extract_svs
#extract_mu_sigma_w=${bin_path}/bin/extract_mu_sigma_w
#calc_ivector=${bin_path}/bin/calc_ivector.py
SVbin2libsvm=${bin_path}/bin/svbin2libsvm.py
UBM=${bin_path}/UBM/jmodel
#TVmatrix=${bin_path}/tvmatrix/tvmatrix_it3.npy
mkdir -p ${bin_path}/tmp

# $wavspklist に空行があれば削除
tempwavspklist=${bin_path}/tmp/wav-spklist_rmspace.txt
grep -v '^\s*$' $wavspklist > $tempwavspklist

# wav を短くカット
cutwavspklist=${bin_path}/tmp/cutwav-spklist.txt
bash $cut_wavbin $tempwavspklist $cutwavspklist ${bin_path}/tmp

# wav --> MFCC
mkdir -p ${bin_path}/mfcc
rm -f ${bin_path}/mfcc/*\.mfcc
cut -f 2 $cutwavspklist > ${bin_path}/tmp/speaker.txt
rm -f ${bin_path}/tmp/mfcc.txt
cut -f 1 $cutwavspklist | while read wav; do
    if [ ! -s $wav ]; then
        echo "Error: $wav does not exist!"
        exit 1
    fi

    segid=$(basename $wav .wav)
    mfcctempfile=${bin_path}/mfcc/${segid}_tmp.mfcc
    mfccfile=${bin_path}/mfcc/${segid}.mfcc
    $HCopybin -T 1 -C $HCopyConf $wav $mfcctempfile
    python3 $global_cmn $mfcctempfile $mfccfile
    rm -f $mfcctempfile
    echo $mfccfile >> ${bin_path}/tmp/mfcc.txt
done

paste ${bin_path}/tmp/mfcc.txt ${bin_path}/tmp/speaker.txt > ${bin_path}/tmp/mfcclist.txt


# MAP 適応で GMM を推定し、SV を抽出
rm -f ${bin_path}/tmp/train.dat
cat ${bin_path}/tmp/mfcclist.txt | while read line; do
    mfccfile=$(echo -e "$line" | cut -f 1)
    speaker=$(echo -e "$line" | cut -f 2)
    echo -e "$mfccfile\t$speaker"

    bash $makeGMMbin $mfccfile $UBM
done
sed -e 's@\/mfcc\/@\/GMM\/@g' -e 's@\.mfcc@@g' ${bin_path}/tmp/mfcc.txt > ${bin_path}/tmp/gmmlist.txt
$extractSVbin $UBM ${bin_path}/tmp/gmmlist.txt ${bin_path}/tmp/svs_bin
python $SVbin2libsvm $(wc -l ${bin_path}/tmp/mfcc.txt | cut -d ' ' -f 1) 3200 ${bin_path}/tmp/svs_bin > ${bin_path}/tmp/train_tmp.dat
paste -d ' ' ${bin_path}/tmp/speaker.txt ${bin_path}/tmp/train_tmp.dat > ${bin_path}/tmp/train.dat


: <<'#__COMMENT__'
# i-vector の計算
mu_ubm=${bin_path}/tmp/mu_ubm.txt
sigma_ubm=${bin_path}/tmp/sigma_ubm.txt
w_ubm=${bin_path}/tmp/w_ubm.txt

$extract_mu_sigma_w $UBM $mu_ubm $sigma_ubm $w_ubm
python ${calc_ivector} ${bin_path}/tmp/mfcc.txt $mu_ubm $sigma_ubm $w_ubm $TVmatrix > ${bin_path}/tmp/train_tmp.dat
paste -d ' ' ${bin_path}/tmp/speaker.txt ${bin_path}/tmp/train_tmp.dat > ${bin_path}/tmp/train.dat

rm -f ${bin_path}/tmp/gmmlist.txt ${bin_path}/tmp/speaker.txt ${bin_path}/tmp/gmmlist.txt ${bin_path}/tmp/svs_bin ${bin_path}/tmp/train_tmp.dat
#__COMMENT__

# SVM を学習
mkdir -p ${bin_path}/SVM
$svmscalebin -s ${bin_path}/SVM/scale.dat ${bin_path}/tmp/train.dat > ${bin_path}/tmp/s_train.dat

## 最適パラメータの探索: Cross validation
for ((power=-10;power<=5;power++)); do
    if [ $power -lt 0 ]; then
        cost=0$(echo "scale=10; 2^${power}" | bc)
    else
        cost=$(echo "scale=10; 2^${power}" | bc)
    fi
    cvresult=${bin_path}/tmp/cv_result_c${power}.txt
    $svmtrainbin -c $cost -v 5 ${bin_path}/tmp/s_train.dat > $cvresult
done
## 最適パラメータの探索: 認識率が一番良くなった cost を探す
maxacc=0
for ((power=-10;power<=5;power++)); do
    cvresult=${bin_path}/tmp/cv_result_c${power}.txt
    curacc=$(grep 'Cross Validation Accuracy' $cvresult | sed -e 's/Cross Validation Accuracy = //g' -e 's/%$//g')
    if [ $(echo "$curacc > $maxacc" | bc) -eq 1 ]; then
        maxacc=$curacc
        maxpower=$power
    fi
done
if [ $maxpower -lt 0 ]; then
    bestcost=0`echo "scale=10; 2^${maxpower}" | bc`
else
    bestcost=`echo "scale=10; 2^${maxpower}" | bc`
fi

echo "Train SVM (cost = 2^${maxpower})"
$svmtrainbin -c $bestcost ${bin_path}/tmp/s_train.dat ${bin_path}/SVM/model

rm -f ${bin_path}/tmp/train.dat ${bin_path}/tmp/s_train.dat

if [ -s ${bin_path}/SVM/model ]; then
    echo -e "\n\n[ Finished training SVM! ]"
fi
