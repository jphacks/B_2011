#!/bin/bash

sudo apt-get install build-essential -y
sudo apt-get install sox -y
sudo apt-get install python3 -y

export LD_LIBRARY_PATH=/usr/local/lib

tar xzvf mecab-0.996.tar.gz
tar xzvf CRF++-0.58.tar.gz
tar xjvf cabocha-0.68.tar.bz2

cd CRF++-0.58
./configure
make
sudo make install
cd -

cd mecab-0.996
./configure --with-charset=utf8
make
sudo make install
cd -

cd cabocha-0.68
./configure --with-charset=UTF8 --with-posset=UNIDIC
make
sudo make install
cd -

