from plyer import notification
import pyperclip
from helperModule import helper
import sys
import os
sys.path.append(os.path.abspath(".."))


def monitor(exam_id, tester_id, tester_name, examinee_id):
    previous = pyperclip.paste()

    while True:
        try:
            now = pyperclip.paste()
            if now != previous:
                previous = now
                helper.send_json(
                    exam_id=exam_id,
                    tester_id=tester_id,
                    tester_name=tester_name,
                    examinee_id=examinee_id,
                    module_name="clipboard",
                    alert="True",
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
