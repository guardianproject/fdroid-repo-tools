#!/bin/sh

set -e
set -x

alias=1
apk=`echo $1| sed s,unsigned,unaligned,`
keydir=`dirname $0`

cp -u $1 $apk

/usr/bin/jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore $keydir/certificate.jks \
    -storepass:file "$keydir/passin.txt" -keypass:file "$keydir/passout.txt" $apk $alias

/usr/bin/jarsigner -verbose -certs -verify $apk -keystore $keydir/certificate.jks \
    -storepass:file "$keydir/passin.txt" -keypass:file "$keydir/passout.txt"
