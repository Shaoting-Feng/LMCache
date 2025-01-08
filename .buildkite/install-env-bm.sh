#!/bin/bash

CONDA_ENV_NAME="buildkite-bm"
PYTHON_VERSION=3.10

exist_env="$(conda env list | grep ${CONDA_ENV_NAME})"
if [[ -n $exist_env ]]; then
    echo "Skipping env creation"
else
    conda create -n ${CONDA_ENV_NAME} python=${PYTHON_VERSION} -y
fi

cuda_version=12.1
export CUDA_HOME=/usr/local/cuda-${cuda_version}
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export PATH=$CUDA_HOME/bin:$PATH

eval "$(conda shell.bash hook)"
conda activate ${CONDA_ENV_NAME}

set -xe 

export LD_LIBRARY_PATH=/dataheart/yihua98/Applications/anaconda3/envs/${CONDA_ENV_NAME}/lib/python3.10/site-packages/nvidia/nvjitlink/lib/:$LD_LIBRARY_PATH 

pip install -r requirements.txt
pip install -r requirements-test.txt
pip install coverage

set +x
echo "Current env:"
pip freeze 
