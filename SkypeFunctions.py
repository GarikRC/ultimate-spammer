import time
import sys
import requests

import Skype4Py
import pyautogui

__author__ = 'Qubasa'

skype = Skype4Py.Skype()


def GetFriends():
    friendlist = {}  # [index][username, status, fullname]
    for i in range(len(skype.Friends)):
        username = skype.Friends[i].Handle  # Handle
        fullname = skype.Friends[i].FullName

        if skype.Friends[i].OnlineStatus in (Skype4Py.olsOnline, Skype4Py.olsInvisible, Skype4Py.olsDoNotDisturb):
            friendlist[i] = ([username, 'ON', fullname])
        else:
            friendlist[i] = ([username, 'OFF', fullname])

    return friendlist


def GetIp(rawSkypeName):
    response = requests.get('http://api.hanzresolver.com/api.php?username=' + rawSkypeName + '&free')
    if response.status_code == requests.codes.ok and response.text.split()[0].encode("ascii") != "Error:":
        ipAddress = response.text.split()[0].encode("ascii")
        return ipAddress
    else:
        return response.text.encode("ascii")


def ClearChat():
        skype.ClearChatHistory()
        skype.Client.Shutdown()
        time.sleep(3)
        skype.Client.Start()


def UploadText(friendlist, target, msg, quantity):

        for i in range(quantity):
            skype.SendMessage(friendlist[target][0], msg)


def AutoTypeText(friendlist, target, msg, quantity):

        skype.Client.Start()
        skype.Client.Focus()
        time.sleep(3)
        for i in range(quantity):
            skype.Client.OpenMessageDialog(friendlist[target][0], msg)
            pyautogui.press('enter')
            time.sleep(0.1)


def DoExit(closeskype):
    if closeskype is True:
        skype.Client.Shutdown()
        sys.exit()
    else:
        sys.exit()