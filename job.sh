#!/bin/zsh

# activate conda environment
source "$(conda info --base)"/etc/profile.d/conda.sh && conda activate icbc

python main.py --pipeline --storage assets/
