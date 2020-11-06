#!/usr/bin/python3

# 入力された mfcc ファイルに global CMN を施す

import sys
import optparse
import numpy as np

D = 26 # 次元数。MFCC_E_D なら 26
D_MFCC = 12 # 生の MFCC の次元数

usage="""usage: %prog infile outfile"""
parser = optparse.OptionParser(usage=usage)
options, args = parser.parse_args()

if not len(args) == 2:
  print("Error: wrong argument", file=sys.stderr)
  parser.print_help()
  exit(1)
mfccfile = args[0]
mfccfile_cmn = args[1]


# MFCC を 配列に格納
# ヘッダは先頭12バイト
mfcc = np.fromfile(mfccfile, dtype='<f4')
header, mfcc = mfcc[:3], mfcc[3:]
nsample = len(mfcc) // D
mfcc = np.reshape(mfcc, (nsample, D))

# MFCC の global mean（ただし、CMN を施すのは生の MFCC の部分だけ）
mfcc_mean = np.mean(mfcc, axis=0)
mfcc_mean[D_MFCC:] = 0 # 生の MFCC 以外の次元はゼロ埋め

# MFCC から global mean を引く
mfcc -= mfcc_mean

# ヘッダを付けて出力
mfcc = np.r_[header, mfcc.flatten()]
mfcc.tofile(mfccfile_cmn)

