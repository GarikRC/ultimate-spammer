# -*- coding: utf-8 -*-
import hashlib
import requests
import platform
import os
import re


__author__ = 'qubasa'

# Variables
if platform.system() == 'Windows':
    pathsign = '\\'
else:
    pathsign = '/'


def CheckRepo(path):

    # https://api.github.com/repos/Qubasa/ultimate-spammer/contents/[filename]
    repolink = 'https://api.github.com/repos/Qubasa/ultimate-spammer/contents/'
    files = os.listdir(path)
    sha1 = hashlib.sha1()
    allowed = ['py', '.md']

    # Exclude unallowed file endings
    for currentfile in files:

        if not currentfile.endswith(tuple(allowed)):
            files.remove(currentfile)

    # Weird bug solution
    if not files[0].endswith(tuple(allowed)):
        files.remove(files[0])

    # Check SHA from files
    for currentfile in files:

        # Get file SHA from Github
        r = requests.get(repolink + currentfile)
        if r.status_code is requests.codes.ok:

            datalist = r.text.split(',')
            checksum = datalist[2].strip('"sha": "').strip('"')

        else:
            print "Connection error " + currentfile + " " + r.text

        # Calculate SHA from local file
        try:
            f = open(path + pathsign + currentfile, 'rb')
            sha1.update(f.read())  # Get SHA with sha1.hexdigest()
        finally:
            f.close()

        if sha1.hexdigest() is not checksum:
            print "[+] " + currentfile + " has to be updated"
