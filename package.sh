#!/bin/sh

if [ ! -f main/python/ijp ]; then
    echo "main/python/ijp not found - change directory"
    exit 1
fi

rm -f *.tar.gz
tar --owner=root --group=root --exclude=".svn" -zcf ijp-utils-1.0.0.tar.gz main README


