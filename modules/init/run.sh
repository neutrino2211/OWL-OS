cd firmware
bash build.sh
cd ../native
node-gyp build
cd ../
node index.js