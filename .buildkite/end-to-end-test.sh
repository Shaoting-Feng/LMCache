#!/bin/bash

cd ../lmcache-tests
python3 main.py tests/tests.py -f test_chunk_prefill -o outputs/
python3 main.py tests/tests.py -f test_lmcache_local_gpu -o outputs/
python3 main.py tests/tests.py -f test_lmcache_local_distributed -o outputs/
python3 main.py tests/tests.py -f test_lmcache_remote_cachegen -o outputs/
cd ../end-to-end-tests/.buildkite
python3 drawing_wrapper.py ../../lmcache-tests/outputs/
mv ../../lmcache-tests/outputs/* ../
