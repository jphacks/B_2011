import sys
import os
sys.path.append(os.path.abspath(".."))
from helperModule import helper

import pyperclip
from plyer import notification

def monitor():
    previous = pyperclip.paste()

    while True:
        try:
            now = pyperclip.paste()
            if now != previous:
                previous = now
                helper.send_str("This guy is copying something!")      
                notification.notify(
                    title="Suspicious action detected!",
                    message="Contents in clipboard changed",
                    app_name="Vega",
                    app_icon="./vega.ico",
                    timeout=3
                )
        except:
            break