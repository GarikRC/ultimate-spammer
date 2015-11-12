# -*- coding: utf-8 -*-
import hashlib
import requests
import os
import time

__author__ = 'Qubasa'


def GitHash(data):
    sha1 = hashlib.sha1()
    sha1.update("blob %u\0" % len(data))
    sha1.update(data)
    return sha1.hexdigest()


def CreateFile(filename):
    if not os.path.isfile(filename):
        f = open(filename, 'wb')
        f.close()


# Index only permitted files in directory
def GetFilesInDir(dirpath, allowedfiles, filterfiles=True):

    files = os.listdir(dirpath)
    excludefiles = []

    if filterfiles:
        # Exclude unallowed file endings
        for currentfile in files:

            if not currentfile.endswith(tuple(allowedfiles)):
                excludefiles.append(currentfile)

        for currentfile in excludefiles:
            files.remove(currentfile)

    return files


# Get date out of saved hashes
def GetLastUpdate(textfilename):

    CreateFile(textfilename)

    saveSHA = open(textfilename, 'rb')
    try:
        if os.path.getsize(textfilename) > 0:   # If file is not empty

            lastupdate = saveSHA.readline().split("|")[0].split(":")[2]   # Get date of first entry

        else:
            lastupdate = None

        return lastupdate

    except Exception, error:
        raise error

    finally:
        saveSHA.close()


# Get hash from Github
def DownloadSHA(filename, shalink, textfilename="saveSHA.txt"):

    CreateFile(textfilename)
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
        raise LookupError("Cant connect to " + shalink + "\n Error: " + r.text)


# Download code and apply patch
def UpdateFile(downloadlink, filename):

    r = requests.get(downloadlink + filename)

    if r.status_code is requests.codes.ok:
        pass
        f = open(filename, "wb")
        f.write(r.text.encode("utf-8"))
    else:
        raise LookupError("Cant connect to " + downloadlink + "\n Error: " + r.text)


# Checks for updates with allowed files in dir return tuple-array (untouchedfiles, updatedfiles)
def PullRepo(files, shalink, downloadlink, applypatch=True, textfilename="saveSHA.txt"):

    # Method variables
    currentdate = time.strftime("%d/%m/%Y")
    lastupdate = GetLastUpdate(textfilename)
    iterations = -1
    untouched = []
    updated = []
    allfiles = (untouched, updated)

    # Delete old text entries in saveSHA
    if currentdate != lastupdate:
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
            if applypatch:
                UpdateFile(downloadlink, currentfile)
                updated.append(currentfile)
            else:
                updated.append(currentfile)
        else:
            untouched.append(currentfile)

    return allfiles



