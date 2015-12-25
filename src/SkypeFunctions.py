# -*- coding: utf-8 -*-
import time
import sys

# third party modules
import requests
import Skype4Py

try:
    import pyautogui

except ImportError:
    pass


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
    if response.status_code is requests.codes.ok and response.text.split()[0].encode("ascii") != "Error:":
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
    try:
        pyautogui.FAILSAFE = True

        skype.Client.Start()
        skype.Client.Focus()
        time.sleep(3)
        for i in range(quantity):
            skype.Client.OpenMessageDialog(friendlist[target][0], msg)
            pyautogui.press('enter')
            time.sleep(0.1)

    except pyautogui.FailSafeException as e:
        raise e


def genericSpammer(quantity, msg):
    try:
        pyautogui.FAILSAFE = True

        for i in range(quantity):
            pyautogui.typewrite(msg, interval=0.001)
            pyautogui.press('enter')

    except pyautogui.FailSafeException as e:
        raise e


def InitSkype():

    try:

        # Starting Skype
        if not skype.Client.IsRunning:  # Creates huge error if you catch the exception
            skype.Client.Start()   # (Minimized=False, Nosplash=False)

        while not skype.Client.IsRunning:
            # Connects to Skype API
            skype.Attach()

        return skype.CurrentUser.FullName

    except Skype4Py.SkypeAPIError as er:
        raise er

    except IOError as er:
        raise er

    except Exception as er:
        raise er
