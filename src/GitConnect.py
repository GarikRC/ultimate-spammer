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
def GetFilesInDir(dirpath, allowedfiles):

    files = os.listdir(dirpath)
    excludefiles = []

    # Exclude unallowed file endings
    for currentfile in files:

        if not currentfile.endswith(tuple(allowedfiles)):
            excludefiles.append(currentfile)

    for currentfile in excludefiles:
        files.remove(currentfile)

    return files


# Get date out of saved hashes
def GetLastUpdate(savesfile):

    CreateFile(savesfile)

    saveSHA = open(savesfile, 'rb')
    try:
        if os.path.getsize(savesfile) > 0:   # If file is not empty

            lastupdate = saveSHA.readline().split("|")[0].split(":")[2]   # Get date of first entry

        else:
            lastupdate = None

        return lastupdate

    except Exception, error:
        raise error

    finally:
        saveSHA.close()


# Get hash from Github (relativepath = Relative to root directory ex. etc/)
def DownloadSHA(filename, shalink, savesfile, relativepath=""):

    CreateFile(savesfile)
    currentdate = time.strftime("%d/%m/%Y")

    r = requests.get(shalink + relativepath + filename)
    if r.status_code is requests.codes.ok:

        datalist = r.text.split(',')
        onlinechecksum = datalist[2].strip('"sha": "').strip('"')
        saveSHA = open(savesfile, 'ab')
        saveSHA.write(filename + ":" + onlinechecksum + ":" + currentdate + "|")
        saveSHA.close()

        return onlinechecksum
    else:
        raise LookupError("Cant connect to " + shalink + relativepath + filename + "\n Error: " + r.text)


# Download code and apply patch
def UpdateFile(downloadlink, dirpath, filename, relativepath=""):

    r = requests.get(downloadlink + relativepath + filename)

    if r.status_code is requests.codes.ok:
        f = open(os.path.join(dirpath, filename), "wb")
        f.write(r.text.encode("utf-8"))
    else:
        raise LookupError("Cant connect to " + downloadlink + relativepath + filename + "\n Error: " + r.text)


# Checks for updates with allowed files in dir return tuple-array (untouchedfiles, updatedfiles)
def PullRepo(dirpath, files, shalink, downloadlink, savesfile, relativepath="", applypatch=True):

    # Method variables
    currentdate = time.strftime("%d/%m/%Y")
    lastupdate = GetLastUpdate(savesfile)
    iterations = -1
    untouched = []
    updated = []
    allfiles = (untouched, updated)

    # Delete old text entries in saveSHA
    if currentdate != lastupdate:
        saveSHA = open(savesfile, 'wb')
        saveSHA.close()

    # Browse all files
    for currentfile in files:

        iterations = iterations + 1

        # Get online hash from Github
        if currentdate != lastupdate:
            onlinechecksum = DownloadSHA(currentfile, shalink, savesfile, relativepath=relativepath)
        else:
            saveSHA = open(savesfile, 'rb')
            onlinechecksum = saveSHA.readline().split("|")[iterations].split(":")[1]
            saveSHA.close()

        # Calculate SHA from file
        f = open(os.path.join(dirpath, currentfile), 'rb')
        localchecksum = GitHash(f.read())
        f.close()

        # Update if necessary
        if localchecksum != onlinechecksum:
            if applypatch:
                UpdateFile(downloadlink, dirpath, currentfile, relativepath)
                updated.append(currentfile)
            else:
                updated.append(currentfile)
        else:
            untouched.append(currentfile)

    return allfiles
