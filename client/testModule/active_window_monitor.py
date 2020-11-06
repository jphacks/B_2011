import sys
import os
sys.path.append(os.path.abspath(".."))
from helperModule import helper

import time

def monitor(exam_id, tester_id, tester_name, examinee_id):
    if sys.platform == "darwin": # for Mac
        pass # To be honest, I don't know much about Mac :/

    elif sys.platform == "win32": # for Windows
        import win32gui

        previous = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        # helper.send_json(
        #     exam_id=exam_id,
        #     tester_id=tester_id,
        #     tester_name=tester_name,
        #     examinee_id=examinee_id,
        #     module_name="window",
        #     alert="False",
        #     description="Active window monitor has started running.",
        #     content=previous
        # )
        # helper.send_str(previous)
        time.sleep(1)

        while True:
            now = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if now != previous:
                previous = now
                helper.send_json(
                    exam_id=exam_id,
                    tester_id=tester_id,
                    tester_name=tester_name,
                    examinee_id=examinee_id,
                    module_name="window",
                    alert="True",
                    description="Active window changed.",
                    content=previous
                )
                # helper.send_str(previous)
            time.sleep(1)