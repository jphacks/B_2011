# If you are trying to add new module, do the following
# 1. add import sentence
# 2. create new thread in main func. it will be called.
# 3. you can use helper func in helper/helper.py

import threading
import logging
# import modules
from testModule import test

def main():
    # create threads
    threads = [
            # threading.Thread(target=test.hoge)
    ]
    # call threads
    for t in threads:
        t.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
    main()

