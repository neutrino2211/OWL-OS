#! /bin/bash
crdir=$(pwd)

cd modules/init
bash build.sh
cd $crdir

cd modules/modules
bash build.sh
cd $crdir

./electron/electron index.js