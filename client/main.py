# If you are trying to add new module, do the following
# 1. add import sentence
# 2. create new thread in main func. it will be called.
# 3. you can use helper func in helper/helper.py

import sys
import threading
import logging
# import modules
from testModule import summon_voice_text_window, clipboard_monitor, active_window_monitor, electron_server, sampling_pics, calc_similarity
from testModule.voice import voice_anomaly_detection

exam_id = "123abc"
examinee_id = "456efg"

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
            threading.Thread(target=calc_similarity.calc_similarity),
            threading.Thread(target=clipboard_monitor.monitor),
            threading.Thread(target=active_window_monitor.monitor),
            threading.Thread(target=electron_server.createServer),
            threading.Thread(target=electron_server.startElectron),
            threading.Thread(target=voice_anomaly_detection.anomaly_detection)
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

