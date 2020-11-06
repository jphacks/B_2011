#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 入力された特徴量系列から Baum-Welch 統計量を計算し、i-vector に変換する
# MSR Identity Toolkit v1.0 の compute_bw_stats.m, extract_ivector.m

import sys
import optparse
#from math import *
import numpy as np
import struct
import time

N_PARTS = 1000

usage="""usage: %prog datalist mu_ubm sigma_ubm w_ubm T_matrix"""
parser = optparse.OptionParser(usage=usage)
options, args = parser.parse_args()

if not len(args) == 5:
  print "Error: wrong argument"
  parser.print_help()
  exit(1)
datalist = args[0]  # 特徴量ファイルパスのリスト
mu_ubm_file = args[1]
sigma_ubm_file = args[2]
w_ubm_file = args[3]
T_matrix = args[4]



def read_HTK_MFCC_E_D_N(feaFilename):
  # MFCC_E_D の特徴量ファイルから MFCC_E_D_N の特徴量を ndim * nframes の配列に格納する (エネルギーを無視)
  # 先頭12バイトがヘッダ
  ndim = 26;

  mfcc = np.fromfile(feaFilename, dtype='<f4')  # リトルエンディアン前提
  nframes = struct.unpack('I', struct.pack('f', mfcc[0]))[0]  # 先頭4バイトがフレーム数
  mfcc = np.reshape(mfcc[3:], [nframes, ndim]).T
  mfcc = np.delete(mfcc, 12, axis=0)  # 第13列がエネルギー
  return mfcc


def expectation(data, mu, sigma, w):
  # compute the sufficient statistics
  post = postprob(data, mu, sigma, w)[0]
  #print "post" # debug
  #print post # debug
  N = np.sum(post, axis=1)
  F = np.dot(data, post.T)
  return (N, F)


def postprob(data, mu, sigma, w):
  # compute the posterior probability of mixtures for each frame
  post = lgmmprob(data, mu, sigma, w)
  llk  = logsumexp(post, 0)
  post = np.exp(post - llk)
  return (post, llk)


def lgmmprob(data, mu, sigma, w):
  # compute the log probability of observations given the GMM
  ndim = np.shape(data)[0]
  C = np.sum(mu**2 * 1./sigma, axis=0) + np.sum(np.log(sigma), axis=0)
  D = np.dot((1./sigma).T, data**2) - 2 * np.dot((mu*1./sigma).T, data) + ndim * np.log(2 * np.pi)
  #print "C"  # debug
  #print C  # debug
  #print "D"  # debug
  #print D  # debug
  logprob = -0.5 * (C[:,np.newaxis] + D)
  #print "logprob1"  # debug
  #print logprob  # debug
  logprob = logprob + np.log(w[:,np.newaxis])
  return logprob


def logsumexp(x, dim):
  # compute log(sum(exp(x),dim)) while avoiding numerical underflow
  xmax = np.max(x, axis=dim)
  y    = xmax + np.log(np.sum(np.exp(x - xmax), axis=dim))
  #ind  = find(~isfinite(xmax))
  #if ~isempty(ind):
  #  y(ind) = xmax(ind)
  return y


def compute_bw_stats(feaFilename, mu_ubm, sigma_ubm, w_ubm):
  ndim, nmix = np.shape(mu_ubm)

  m = np.reshape(mu_ubm.T, ndim*nmix)
  idx_sv = np.reshape(np.tile(np.arange(nmix), [ndim, 1]).T, ndim*nmix)

  # feaFilename を読んで特徴量系列を data に格納
  #data = np.loadtxt(feaFilename, delimiter=' ')
  data = read_HTK_MFCC_E_D_N(feaFilename)

  N, F = expectation(data, mu_ubm, sigma_ubm, w_ubm)
  F = np.reshape(F.T, ndim*nmix)
  F = F - N[idx_sv] * m
  return (N, F)



# -------------------- ここから main --------------------
# UBM の平均 mu_ubm, 分散 sigma_ubm を読む
mu_ubm = np.loadtxt(mu_ubm_file, delimiter=' ')
sigma_ubm = np.loadtxt(sigma_ubm_file, delimiter=' ')
w_ubm = np.loadtxt(w_ubm_file, delimiter=' ')

ndim, nmix = np.shape(mu_ubm);
S = np.reshape(sigma_ubm.T, [ndim*nmix, 1])
idx_sv = np.reshape(np.tile(np.arange(nmix), [ndim, 1]).T, ndim*nmix)

# Total variability matrix T を読む
T = np.load(T_matrix)
if np.shape(T)[0] > np.shape(T)[1]:
  T = T.T
tv_dim = np.shape(T)[0]

I = np.identity(tv_dim)
T_invS =  T / S.T

# 特徴量ファイルパスのリスト
f_list = np.loadtxt(datalist, dtype='S100')
nfiles = np.size(f_list)

# N, F の計算
#N = np.zeros([nfiles, nmix])
#F = np.zeros([nfiles, ndim*nmix])
iv = np.zeros([nfiles, tv_dim])
for ix in range(nfiles):
  #N[ix, :], F[ix, :] = compute_bw_stats(f_list[ix], mu_ubm, sigma_ubm, w_ubm)
  if nfiles == 1:
    N, F = compute_bw_stats(f_list.tolist(), mu_ubm, sigma_ubm, w_ubm)
  else:
    N, F = compute_bw_stats(f_list[ix], mu_ubm, sigma_ubm, w_ubm)

  L = I + np.dot(T_invS*N[idx_sv], T.T)
  B = np.dot(T_invS, F)
  iv[ix, :] = np.dot(np.linalg.pinv(L), B)

  # i-vector を libsvm 形式で出力
  for j in range(tv_dim):
    sys.stdout.write(str(j+1)+":"+str(iv[ix, j])+" ")
  sys.stdout.write("\n")


# i-vector リストを libsvm 形式で出力
#for i in range(nfiles):
#  for j in range(tv_dim):
#    sys.stdout.write(str(j+1)+":"+str(iv[i, j])+" ")
#  sys.stdout.write("\n")
