#!/bin/sh

webroot=/home/members/nfreitas/sites/guardianproject.info/web
fdroidbase=$webroot/fdroid
fdroidrepo=$fdroidbase/repo

cd $fdroidrepo
for f in `find ../../releases/ -type f -name \*.apk`; do
    # if its not in repo/ or archive/, make a hard link in repo/
    test -e $(basename $f) || test -e ../archive/$(basename $f) || \
        ln $f
done
