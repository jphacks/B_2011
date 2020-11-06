import sys
import os
sys.path.append(os.path.abspath(".."))
from helperModule import helper

from plyer import notification
import pyperclip

def monitor():
    previous = pyperclip.paste()

    while True:
        try:
            now = pyperclip.paste()
            if now != previous:
                previous = now
                helper.send_json(
                    module_name="clipboard",
                    alert=True,
                    description="This guy is copying something!",
                    content=previous
                )
                notification.notify(
                    title="Suspicious action detected!",
                    message="Contents in clipboard changed",
                    app_name="Vega",
                    app_icon="./vega.ico",
                    timeout=3
                )
        except:
            break
