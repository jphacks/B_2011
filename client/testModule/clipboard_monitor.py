import sys
import os
sys.path.append(os.path.abspath(".."))
from helperModule import helper

import pyperclip

def monitor():
    previous = pyperclip.paste()

    while True:
        try:
            now = pyperclip.paste()
            if now != previous:
                previous = now
                helper.send_str("This guy is copying something!")      
        except:
            break