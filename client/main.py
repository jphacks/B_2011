# If you are trying to add new module, do the following
# 1. add import sentence
# 2. create new thread in main func. it will be called.
# 3. you can use helper func in helper/helper.py

import sys
import threading
import logging
# import modules
from testModule import test, summon_voice_text_window, clipboard_monitor, active_window_monitor

def terminate():
    while True:
        try:
            pass
        except KeyboardInterrupt:
            sys.exit(0)

def main():
    # record voice first
    summon_voice_text_window.record()

    # create threads
    threads = [
            threading.Thread(target=test.hoge),
            threading.Thread(target=clipboard_monitor.monitor),
            threading.Thread(target=active_window_monitor.monitor)
    ]
    # call threads
    for t in threads:
        t.setDaemon(True)
        t.start()
    # make Ctrl+C kill all processes
    terminate()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
    main()

