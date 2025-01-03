#!/bin/bash

rm -rf ../lmcache-vllm
git clone https://github.com/LMCache/lmcache-vllm.git ../lmcache-vllm
cd ../lmcache-vllm
pip install .

rm -rf ../lmcache-tests
git clone https://github.com/LMCache/lmcache-tests.git ../lmcache-tests

pip install matplotlib
