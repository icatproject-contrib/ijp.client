#!/bin/sh

if [ ! -f main/python/ijp ]; then
    echo "main/python/ijp not found - change directory"
    exit 1
fi

if [ $(find -maxdepth 0 -name *.tar.gz | wc -l) -eq 0 ]; then
    tar --owner=root --group=root --exclude=".svn" -zcf ijp-utils-1.0.0.tar.gz main README
elif [ $(find -newer *.tar.gz -type f | wc -l) -ne 0 ]; then
    rm -f *.tar.gz
    tar --owner=root --group=root --exclude=".svn" -zcf ijp-utils-1.0.0.tar.gz main README
fi

