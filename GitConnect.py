# -*- coding: utf-8 -*-
import hashlib
import requests
import os
import time


__author__ = 'qubasa'


def GitHash(data):
    sha1 = hashlib.sha1()
    sha1.update("blob %u\0" % len(data))
    sha1.update(data)
    return sha1.hexdigest()


# Index only permitted files in directory
def GetFilesInDir(dirpath, allowedfiles, filterfiles=True):

    files = os.listdir(dirpath)

    if filterfiles:
        # Exclude unallowed file endings
        for currentfile in files:

            if not currentfile.endswith(tuple(allowedfiles)):
                files.remove(currentfile)

        # Repeat if not done some .pyc files remain (bug ?)
        for currentfile in files:

            if not currentfile.endswith(tuple(allowedfiles)):
                files.remove(currentfile)

    return files


# Get date out of saved hashes
def GetLastUpdate(textfilename, currentdate):

    saveSHA = open(textfilename, 'rb')
    if os.path.getsize(textfilename) > 0:   # If file is not empty

        filedate = saveSHA.readline().split("|")[0].split(":")[2]   # Get date of first entry
        print "Filedate: " + filedate + " Currentdate: " + currentdate

    else:
        filedate = None
        print "No entries were detected"
    saveSHA.close()
    return filedate


# Get hash from Github
def DownloadSHA(filename, shalink, textfilename="saveSHA.txt"):

    currentdate = time.strftime("%d/%m/%Y")

    r = requests.get(shalink + filename)
    if r.status_code is requests.codes.ok:

        datalist = r.text.split(',')
        onlinechecksum = datalist[2].strip('"sha": "').strip('"')
        saveSHA = open(textfilename, 'ab')
        saveSHA.write(filename + ":" + onlinechecksum + ":" + currentdate + "|")
        saveSHA.close()

        return onlinechecksum
    else:
        print "Connection error " + filename + " " + r.text


# Download code and apply patch
def UpdateFile(downloadlink, filename):

    response = requests.get(downloadlink + filename)

    if response.status_code is requests.codes.ok:
        code = response.text.encode("utf-8")
        #f = open(filename, "wb")
        #f.write(code)
        print "[+] Done updating " + filename
        print
    else:
        print "[-] Error downloading file!"


def CheckRepo(files, shalink, downloadlink, textfilename="saveSHA.txt"):

    # Method variables
    currentdate = time.strftime("%d/%m/%Y")
    lastupdate = GetLastUpdate(textfilename, currentdate)
    iterations = -1

    # Delete old text entries in saveSHA
    if currentdate != lastupdate:
        print "Delete old Entries"
        saveSHA = open(textfilename, 'wb')
        saveSHA.close()

    # Browse all files
    for currentfile in files:

        iterations = iterations + 1

        # Get online hash from Github
        if currentdate != lastupdate:
            onlinechecksum = DownloadSHA(currentfile, shalink)
        else:
            saveSHA = open(textfilename, 'rb')
            onlinechecksum = saveSHA.readline().split("|")[iterations].split(":")[1]
            saveSHA.close()

        # Calculate SHA from file
        f = open(currentfile, 'rb')
        localchecksum = GitHash(f.read())
        f.close()

        # Update if necessary
        if localchecksum != onlinechecksum:
            print "[-] " + currentfile + " has to be updated"
            UpdateFile(downloadlink, currentfile)
        else:
            print "[+] Already up to date: " + currentfile


