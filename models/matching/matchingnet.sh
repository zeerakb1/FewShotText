#!/usr/bin/env bash
cd $HOME/FewShotText
source .venv/bin/activate
source .envrc
echo "CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES}"
command -v nvidia-smi >/dev/null && {
    echo "GPU Devices:"
    nvidia-smi
} || {
    :
}

# Check if numpy can be imported
python -c "import numpy; print('Numpy imported successfully')"

PYTHONPATH=. python models/matching/matchingnet.py $@
