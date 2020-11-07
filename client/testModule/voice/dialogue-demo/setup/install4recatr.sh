#!/bin/bash

bin_path=$(dirname $(readlink -f $0))
curdir=$(pwd)

cd ${bin_path}/source
tar xzvf ${bin_path}/source/julius-4.2.2.tar.gz

cd ${bin_path}/source/julius-4.2.2
./configure
sudo make install
cd $curdir

sudo apt-get install sox
sudo modprobe -v snd-pcm-oss
