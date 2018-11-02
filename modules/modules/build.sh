#! /bin/sh
dir=`pwd`
function build_dir {
    for dname in `ls $1` ; do
        if [[ -d $1/$dname ]] ; then
            if [[ -e $1/$dname/link ]] ; then
                build_dir $1/$dname
            fi
            if [[ -e $1/$dname ]] ; then
                for fname in `ls $1/$dname | grep .cc`; do
                    if [[ -e $1/$dname/build ]] ; then
                        g++  -fPIC -shared $1/$dname/$fname -o $1/$dname/build/${fname%.cc}.so
                    else 
                        mkdir -p $1/$dname/build
                        g++  -fPIC -shared $1/$dname/$fname -o $1/$dname/build/${fname%.cc}.so
                    fi
                    echo "Built module $fname"
                done   
            fi
        fi
    done
}

build_dir `pwd`