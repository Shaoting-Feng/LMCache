#!/bin/bash

pip install -e .

cd ../lmcache-vllm
git pull

cd ../lmcache-tests
git pull

pip install matplotlib
