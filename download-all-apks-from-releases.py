#!/usr/bin/env python

import binascii
import os
import tempfile
import urllib2
from BeautifulSoup import BeautifulSoup
import pprint


def download_all_apks_and_sigs(url, dldir):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)

    for link in soup.html.body.findAll('a'):
        apklink = link.get('href')
        if not apklink.endswith('.apk'):
            continue
        if apklink.endswith('-latest.apk'): # these are just symlinks
            continue
        if apklink[0] != '/' and not apklink.startswith('http'):
            apklink = url + '/' + apklink
        print(apklink)
        apkasc = None
        apksig = None
        try:
            apk = urllib2.urlopen(apklink).read()
            apkname = os.path.basename(apklink)
            with open(os.path.join(dldir, apkname), 'w') as f:
                f.writelines(apk)
            apkasc = urllib2.urlopen(apklink + '.asc').read()
            with open(os.path.join(dldir, apkname + '.asc'), 'w') as f:
                f.writelines(apkasc)
        except urllib2.HTTPError as e:
            try:
                apksig = urllib2.urlopen(apklink + '.sig').read()
                with open(os.path.join(dldir, apkname + '.sig'), 'w') as f:
                    f.writelines(apksig)
            except urllib2.HTTPError as e:
                print(os.path.basename(apklink) + ' has no signature file!')
                print(e)


tmpdir = tempfile.mkdtemp(prefix='.gp-releases-audit-')
print('its all in ' + tmpdir)

download_all_apks_and_sigs('https://guardianproject.info/releases', tmpdir)
download_all_apks_and_sigs('https://guardianproject.info/releases/archive', tmpdir)
