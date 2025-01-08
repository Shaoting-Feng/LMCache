#!/bin/bash

set -xe 

pip uninstall -y lmcache
pip cache purge
pip install -e .

pip show lmcache
