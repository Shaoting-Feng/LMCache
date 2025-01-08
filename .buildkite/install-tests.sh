#!/bin/bash

pip uninstall -y lmcache-vllm
rm -rf ../lmcache-vllm
git clone https://github.com/LMCache/lmcache-vllm.git ../lmcache-vllm
cd ../lmcache-vllm
git fetch --all
git reset --hard origin/dev
pip cache purge
pip install -e .

rm -rf ../lmcache-tests
git clone https://github.com/LMCache/lmcache-tests.git ../lmcache-tests

pip install matplotlib
