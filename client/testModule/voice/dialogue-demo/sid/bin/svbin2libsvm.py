#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 入力されたスーパーベクトルを libsvm の形式で出力

import sys
import optparse
import numpy as np
import time


usage="""usage: %prog ndata dimension infile w_matrix"""
parser = optparse.OptionParser(usage=usage)
options, args = parser.parse_args()

if not len(args) == 3:
  print "Error: wrong argument"
  parser.print_help()
  exit(1)
ndata = int(args[0])  # データ数
dim = int(args[1])  # スーパーベクトルの次元数
infile = args[2]


# データを配列に格納
# x: データ数×次元数
x = np.fromfile(infile, dtype='float64')
x = np.reshape(x, (ndata, dim))

# libsvm 形式で出力
for i in range(ndata):
  for j in range(dim):
    sys.stdout.write(str(j+1)+":"+str(x[i][j])+" ")
  sys.stdout.write("\n")
