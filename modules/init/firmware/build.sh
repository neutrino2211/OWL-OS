for dname in `ls ./` ; do
    if [[ -d $dname ]] ; then
        for fname in `ls ./$dname | grep .cc`; do
            if [[ -e ./$dname/build ]] ; then
                g++ -fPIC -shared ./$dname/$fname -o ./$dname/build/${fname%.cc}.so
            else 
                mkdir -p ./$dname/build
                g++ -fPIC -shared ./$dname/$fname -o ./$dname/build/${fname%.cc}.so
            fi
            echo "Built $fname"
        done
    fi
done