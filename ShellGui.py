import os
import platform

from SkypeFunctions import *
from SocialPlattformFunctions import *
from EmailFunctions import *

__author__ = 'Qubasa'

systemOS = platform.system()

if systemOS == 'Windows':
    clearCommand = 'cls'
else:
    clearCommand = 'clear'


def Empty(value):
    if value == "":
        raise ValueError("The Variable is empty!")


def MainMenu():
    os.system(clearCommand)

    print '''
 [*] ULTIMATE SPAMMER 2.0 [*]

            .-------.
      _|~~ ~~  |_
    =(_|_______|_)=
      |:::::::::|
      |:::::::[]|
      |o=======.|
      `"""""""""`

    Creator: Qubasa
-------------------------------

1) Skype uploading text

2) Skype automated typing

3) Clear skype chat

4) Get Ip of skype friend

5) WhatsApp Web automated typing

6) Facebook automated typing

7) Email spammer

99) Quit
    '''
    try:
        choice = raw_input('>> ')
        Exec_Menu(choice)

    except KeyboardInterrupt:
        os.system(clearCommand)
        if skype.Client.IsRunning:
            choice = raw_input("Do you wan to close skype ?[y/n]")
            if choice == "y":
                DoExit(True)
            else:
                DoExit(False)
        else:
            DoExit(False)


def InitSkype():

    try:
        # Starting Skype
        if not skype.Client.IsRunning:  # Creates huge error if you catch the exception
            skype.Client.Start(True)   # (Minimized=False, Nosplash=False)

        print "Please wait a moment..."
        print

        time.sleep(3)

        if skype.Client.IsRunning:
            # Connects to Skype API
            skype.Attach()
            print '[+] Connected to Skype Account: ' + skype.CurrentUser.FullName
            print

    except Skype4Py.SkypeAPIError:
        print "[-] Programm couldn't connect to skype. Please whitelist this programm in skype!"
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()


def GetIpAddress():

    InitSkype()

    try:
        friendlist = GetFriends()
        FriendMenu(friendlist)

    except Skype4Py.SkypeError:
        print "[-] Skype raised an unexpected problem, please try again."
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()

    except Skype4Py.SkypeAPIError:
        print "[-] Connection issues with skype. Is this programm whitelisted ?"
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()

    while True:
        try:
            print 'Target number:'
            target = raw_input('>> ')
            target = int(target)

            if friendlist[target][2] == '':
                x = 0
            else:
                x = 2

            print "The IP of " + friendlist[target][x] + " is: " + GetIp(friendlist[target][0])
            raw_input("Press any key to continue...")
            menu_actions['main_menu']()
        except ValueError:
            print
            print '[-] Invalid input please try again!'
            print
        except KeyError:
            print
            print "[-] This target doesnt exist!"
            print
        except KeyboardInterrupt:
            print "[+] Aborted programm"
            raw_input("Press any key to continue...")
            menu_actions['main_menu']()


def UploadTextMenu():

    InitSkype()

    try:
        friendlist = GetFriends()
        FriendMenu(friendlist)
        target, msg, quantity = InputForm()
        UploadText(friendlist, target, msg, quantity)
        print "[+] Successfully send " + str(quantity) + " messages!"

    except Skype4Py.SkypeError:
        print "[-] Skype raised an unexpected problem, please try again."

    except Skype4Py.SkypeAPIError:
        print "[-] Connection issues with skype. Is this programm whitelisted ?"

    finally:
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()


def AutoTypeTextMenu():

    InitSkype()

    try:
        friendlist = GetFriends()
        FriendMenu(friendlist)
        target, msg, quantity = InputForm()
        AutoTypeText(friendlist, target, msg, quantity)
        print "[+] Successfully send " + str(quantity) + " messages!"

    except Skype4Py.SkypeError:
        print "[-] Skype raised an unexpected problem, please try again."

    except Skype4Py.SkypeAPIError:
        print "[-] Connection issues with skype. Is this programm whitelisted ?"

    finally:
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()


def ClearChatMenu():

    InitSkype()

    try:
        choice = raw_input("Are you sure to delete ALL history ?[y/n]")
        if choice == "y":
            ClearChat()
            print "[+] Done!"
            raw_input("Press any key to continue...")
            menu_actions['main_menu']()
        else:
            raw_input("Press any key to continue...")
            menu_actions['main_menu']()

    except Skype4Py.SkypeError:
        print "[-] Skype raised an unexpected problem, please try again."

    except Skype4Py.SkypeAPIError:
        print "[-] Connection issues with skype. Is this programm whitelisted ?"

    finally:
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()


def DoExitMenu():
    if skype.Client.IsRunning:
        choice = raw_input("Do you wan to close skype ?[y/n]")
        if choice == "y":
            DoExit(True)
        else:
            DoExit(False)
    else:
        DoExit(False)


def Exec_Menu(choice):
    os.system(clearCommand)
    if choice == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[choice]()
        except KeyError:
            print '[-] Invalid selection, please try again.'
            time.sleep(1)
            menu_actions['main_menu']()


def InputForm():
    while True:
        try:
            print 'Target number:'
            target = raw_input('>> ')
            target = int(target)

            print 'Your message to deliver:'
            msg = raw_input('>> ')
            Empty(msg)

            print 'How many times: '
            quantity = raw_input('>> ')
            quantity = int(quantity)
            print
            return target, msg, quantity

        except ValueError:
            print
            print '[-] Invalid input please try again!'
            print
        except KeyboardInterrupt:
            print "[+] Aborted programm"
            raw_input("Press any key to continue...")
            menu_actions['main_menu']()


def FriendMenu(friendlist):
    for index in friendlist:
        if friendlist[index][2] == '':
            x = 0
        else:
            x = 2
        print str(index) + ') ' + friendlist[index][x] + ' : ' + friendlist[index][1]
    print


def WhatsAppSpammerMenu():
    while True:
        try:
            print 'Target name:'
            target = raw_input('>> ')
            Empty(target)

            print 'Your message to deliver:'
            msg = raw_input('>> ')
            Empty(msg)

            print 'How many times: '
            quantity = raw_input('>> ')
            quantity = int(quantity)
            print
            break
        except ValueError:
            print
            print '[-] Invalid input please try again!'
            print
        except KeyboardInterrupt:
            print "[+] Aborted programm"
            raw_input("Press any key to continue...")
            menu_actions['main_menu']()

    try:
        WhatsAppSpammer(target, msg, quantity)
        print '[+] Sucessfully send ' + quantity + " messages to " + target

    except TimeoutException:
        print '[-] Timout error: Something took too long '

    except KeyboardInterrupt:
        print '[+] Aborted programm'

    except NoSuchElementException:
        print '[-] An element id is missing or has been changed'

    except IndexError:
        print '[-] Wrong target name / Please chat with the target least once.'

    finally:
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()


def FacebookSpammerMenu():
    while True:
        try:
            print 'Your Email:'
            email = raw_input('>> ')
            Empty(email)

            print 'Your Password'
            password = raw_input('>> ')
            Empty(password)

            print 'Target name:'
            target = raw_input('>> ')
            Empty(target)

            print 'Your message to deliver:'
            msg = raw_input('>> ')
            Empty(msg)

            print 'How many times: '
            quantity = raw_input('>> ')
            quantity = int(quantity)
            print
            break
        except ValueError:
            print
            print '[-] Invalid input please try again!'
            print
        except KeyboardInterrupt:
            print "[+] Aborted programm"
            raw_input("Press any key to continue...")
            menu_actions['main_menu']()

    try:
        FacebookSpammer(email, password, target, msg, quantity)
        print '[+] Sucessfully send ' + str(quantity) + " messages to " + target

    except TimeoutException:
        print '[-] Timout error: Something took too long '

    except KeyboardInterrupt:
        print '[+] Aborted programm'

    except NoSuchElementException:
        print '[-] An element id is missing or has been changed'

    finally:
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()


def EmailSpammerMenu():

    # server_dictionary[index][name][dnsname][port]
    server_dictionary = {

        1: ['Gmail', 'smtp.gmail.com', 587],
        2: ['Gmx', 'mail.gmx.net', 465],
        3: ['Icloudmail', 'smtp.mail.me.com', 587],
        4: ['Mail.de', 'smtp.mail.de', 587],
        5: ['Outlook', 'smtp-mail.outlook.com', 587],
        6: ['Yahoomail', 'smtp.mail.yahoo.com', 465],
        7: ['Web.de', 'smtp.web.de', 587],
        8: ['Sxmail', 'smtp.sxmail.de', 587]
    }

    for index in range(len(server_dictionary)):
        print str(index + 1) + ") " + server_dictionary[index + 1][0]

    print
    print "Choose server:"
    while True:
        try:
            choice = raw_input(">> ")
            print
            choice = int(choice)
            server = server_dictionary[choice][1]
            port = server_dictionary[choice][2]
            break
        except ValueError:
            print
            print '[-] Invalid input please try again!'
            print
        except KeyError:
            print
            print '[-] Invalid selection please try again!'
            print

    while True:
        try:
            print 'Your Email:'
            username = raw_input('>> ')
            Empty(username)

            print 'Your Password:'
            password = raw_input('>> ')
            Empty(password)

            print 'Target email:'
            targetemail = raw_input('>> ')
            Empty(targetemail)

            print 'Who send this email (From:) ?'
            fromemail = raw_input('>> ')
            Empty(fromemail)

            print 'Subject of this email:'
            subject = raw_input('>> ')
            Empty(subject)

            print 'Your message to deliver:'
            msg = raw_input('>> ')
            Empty(msg)

            print 'How many times: '
            quantity = raw_input('>> ')
            quantity = int(quantity)
            print
            break
        except ValueError:
            print
            print '[-] Invalid input please try again!'
            print
        except KeyboardInterrupt:
            print "[+] Aborted programm."
            raw_input("Press any key to continue...")
            menu_actions['main_menu']()

    try:
        EmailSpammer(server, port, username, password, targetemail, fromemail, subject, msg, quantity)
        print '[+] Sucessfully send ' + str(quantity) + " messages to " + targetemail

    except smtplib.SMTPAuthenticationError:
        print "[-] Log in credentials are wrong."

    except smtplib.SMTPConnectError:
        print "[-] Couldnt connect to server."

    except smtplib.SMTPRecipientsRefused:
        print "[-] Target doesnt exist."

    except smtplib.SMTPException:
        print "[-] An unexpected error was raised, please try again."

    finally:
        raw_input("Press any key to continue...")
        menu_actions['main_menu']()


menu_actions = {
    'main_menu': MainMenu,
    '1': UploadTextMenu,
    '2': AutoTypeTextMenu,
    '3': ClearChatMenu,
    '4': GetIpAddress,
    '5': WhatsAppSpammerMenu,
    '6': FacebookSpammerMenu,
    '7': EmailSpammerMenu,
    '99': DoExitMenu,
}

if __name__ == '__main__':
    menu_actions['main_menu']()
