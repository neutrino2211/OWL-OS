#! /bin/bash
crdir=$(pwd)

cd modules
bash build.sh
cd $crdir

python3 index.py