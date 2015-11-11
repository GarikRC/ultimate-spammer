# -*- coding: utf-8 -*-
import hashlib
import requests
import platform
import os
import time


__author__ = 'qubasa'


def CheckRepo(dirpath):

    # Method variables
    downloadlink = 'https://raw.githubusercontent.com/Qubasa/ultimate-spammer/master/'  # [file]
    repolink = 'https://api.github.com/repos/Qubasa/ultimate-spammer/contents/'
    files = os.listdir(dirpath)
    textfilename = "saveSHA.txt"
    sha1 = hashlib.sha1()
    allowed = ['py', '.md']
    currentdate = time.strftime("%d/%m/%Y")
    iterations = -1

    # Exclude unallowed file endings
    for currentfile in files:

        if not currentfile.endswith(tuple(allowed)):
            files.remove(currentfile)

    # Repeat if not done some .pyc files remain (bug ?)
    for currentfile in files:

        if not currentfile.endswith(tuple(allowed)):
            files.remove(currentfile)

    print files

    # Get date out of saveSHA file
    saveSHA = open(textfilename, 'rb')     # Read file
    if os.path.getsize(os.path.join(dirpath, textfilename)) > 0:   # If it is not empty

        filedate = saveSHA.readline().split("|")[0].split(":")[2]   # Get date of first entry
        print "Filedate: " + filedate + " Currentdate: " + currentdate

    else:
        filedate = None
        print "No entries were detected"
    saveSHA.close()

    # Delete old text entries
    if currentdate != filedate:
        print "Delete old Entries"
        saveSHA = open(textfilename, 'wb')
        saveSHA.close()

    # Check SHA from files
    for currentfile in files:

        iterations = iterations + 1

        # Get Github SHA and write to file
        if currentdate != filedate:

            # Get file SHA from Github
            r = requests.get(repolink + currentfile)
            if r.status_code is requests.codes.ok:

                datalist = r.text.split(',')
                checksum = datalist[2].strip('"sha": "').strip('"')
                saveSHA = open(textfilename, 'ab')
                saveSHA.write(currentfile + ":" + checksum + ":" + currentdate + "|")
                saveSHA.close()
                print "Download Sha"

            else:
                print "Connection error " + currentfile + " " + r.text
        else:
            saveSHA = open(textfilename, 'rb')
            checksum = saveSHA.readline().split("|")[iterations].split(":")[1]
            saveSHA.close()

        # Calculate SHA from local file
        try:
            f = open(textfilename, 'rb')
            #  Get SHA with sha1.hexdigest()
            sha1.update("blob " + str(os.path.getsize(textfilename)) + f.read())

        finally:
            f.close()

        if sha1.hexdigest() is not checksum:
            print "[+] " + currentfile + " has to be updated"
            print "Githubhash: " + checksum
            print "Localhash:  " + sha1.hexdigest()
            print

    saveSHA.close()
