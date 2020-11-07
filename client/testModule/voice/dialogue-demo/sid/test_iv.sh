#! /bin/bash

bin_path=$(dirname $(readlink -f $0))
HCopybin=${bin_path}/../bin/HCopy
svmscalebin=svm-scale
svmpredictbin=svm-predict

if [ $# -ne 2 ]; then
    echo "Usage: $ bash $0 (wav file) (outputdir)"
    exit 1;
fi


# SVM をテストし、推定された話者番号を出力する

wav=$1
HCopyConf=${bin_path}/config/config.HCopy
global_cmn=${bin_path}/bin/global_cmn.py
#makeGMMbin=${bin_path}/bin/makeGMM.sh
#extractSVbin=${bin_path}/bin/extract_svs
extract_mu_sigma_w=${bin_path}/bin/extract_mu_sigma_w
calc_ivector=${bin_path}/bin/calc_ivector.py
UBM=${bin_path}/UBM/jmodel
TVmatrix=${bin_path}/tvmatrix/tvmatrix_it3.npy
mkdir -p ${bin_path}/tmp

# wav --> MFCC
mkdir -p ${bin_path}/mfcc
#rm -f ./mfcc/*\.mfcc
segid=$(basename $wav .wav)
mfcctempfile=${bin_path}/mfcc/${segid}_tmp.mfcc
mfccfile=${bin_path}/mfcc/${segid}.mfcc
$HCopybin -C $HCopyConf $wav $mfcctempfile
python3 $global_cmn $mfcctempfile $mfccfile
rm -f $mfcctempfile

: <<'#__COMMENT__'
# MAP 適応で GMM を推定し、SV を抽出
bash $makeGMMbin $mfccfile $UBM > /dev/null
echo $mfccfile | sed -e 's@\/mfcc\/@\/GMM\/@g' -e 's@\.mfcc@@g' > ${bin_path}/tmp/gmmlist.txt
$extractSVbin $UBM ${bin_path}/tmp/gmmlist.txt ${bin_path}/tmp/svs_bin
python $calc_ivector 1 3200 ${bin_path}/tmp/svs_bin ${bin_path}/wmatrix/wmatrix.npy > ${bin_path}/tmp/test_tmp.dat
echo "1" > ${bin_path}/tmp/speaker.txt
paste -d ' ' ${bin_path}/tmp/speaker.txt ${bin_path}/tmp/test_tmp.dat > ${bin_path}/tmp/test.dat

rm -f ${bin_path}/tmp/speaker.txt ${bin_path}/tmp/gmmlist.txt ${bin_path}/tmp/svs_bin ${bin_path}/tmp/test_tmp.dat
#__COMMENT__


# i-vector の計算
mu_ubm=${bin_path}/tmp/mu_ubm.txt
sigma_ubm=${bin_path}/tmp/sigma_ubm.txt
w_ubm=${bin_path}/tmp/w_ubm.txt

$extract_mu_sigma_w $UBM $mu_ubm $sigma_ubm $w_ubm
echo $mfccfile > ${bin_path}/tmp/mfcc.txt
python ${calc_ivector} ${bin_path}/tmp/mfcc.txt $mu_ubm $sigma_ubm $w_ubm $TVmatrix > ${bin_path}/tmp/test_tmp.dat
echo "1" > ${bin_path}/tmp/speaker.txt
paste -d ' ' ${bin_path}/tmp/speaker.txt ${bin_path}/tmp/test_tmp.dat > ${bin_path}/tmp/test.dat

rm -f ${bin_path}/tmp/gmmlist.txt ${bin_path}/tmp/speaker.txt ${bin_path}/tmp/gmmlist.txt ${bin_path}/tmp/svs_bin ${bin_path}/tmp/train_tmp.dat


# SVM をテスト
mkdir -p ${bin_path}/SVM
$svmscalebin -r ${bin_path}/SVM/scale.dat ${bin_path}/tmp/test.dat > ${bin_path}/tmp/s_test.dat
$svmpredictbin ${bin_path}/tmp/s_test.dat ${bin_path}/SVM/model ${bin_path}/tmp/result.dat > /dev/null

#cat ${bin_path}/tmp/result.dat
cp ${bin_path}/tmp/result.dat $2
rm -f ${bin_path}/tmp/test.dat ${bin_path}/tmp/s_test.dat ${bin_path}/tmp/result.dat 
