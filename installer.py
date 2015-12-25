# -*- coding: utf-8 -*-
import os
import sys

from src import ez_setup


# Install Modules
def install_module(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        try:
            import pip
            pip.main(['install', package])
        except ImportError:
            print "[-] Pip has to be installed. Installation aborted"
            raw_input("Press any key to continue...")
            sys.exit(1)
        # finally:
            # globals()[package] = importlib.import_module(package)


def Main():
    print """

Needed third party tools:
1) Skype
2) Firefox

This programm will install the needed python modules for
the ultimate spammer to work. Included is:
1) skype4py
2) selenium
3) requests
4) pyautogui
5) pillow

On OSX added are also:
1) pyobjc-core
2) pyobjc

On Linux added are also:
1) python-Xlib
    """

    raw_input("Press enter to continue installation...")

    ez_setup.main()
    if sys.platform.startswith("linux"):
        os.system("easy_install pip")

    elif sys.platform.startswith("win"):
        exec_path = os.path.join(sys.exec_prefix + "Scripts" + "easy_install")
        os.system(exec_path + " pip")

    elif sys.platform.startswith("darwin"):
        exec_path = os.path.join(sys.exec_prefix + "Scripts" + "easy_install")
        os.system(exec_path + " pip")

    try:
        install_module('Skype4Py')

    except Exception as er:
            print "[-] Installation of Skype4Py failed: " + str(er)

    try:
        install_module('selenium')

    except Exception as er:
        print "[-] Installation of selenium failed: " + str(er)

    try:
        install_module('requests')

    except Exception as er:
        print "[-] Installation of requests failed: " + str(er)

    try:
        install_module("Pillow")

        # OSX dependencies
        if sys.platform.startswith("darwin"):
            install_module("pyobjc-core")
            install_module("pyobjc")

        # Linux
        if sys.platform.startswith("linux"):
            install_module("python-Xlib")

        install_module('pyautogui')

    except Exception as er:
        print "[-] Installation of pyautogui failed: " + str(er)

    raw_input("[+] Finished, to start the programm run ShellGui.py")

if __name__ == '__main__':
    Main()
