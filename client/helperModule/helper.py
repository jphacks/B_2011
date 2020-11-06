import logging
import json


# TODO: send string to server
# temporarily, use logging.debug

# send string data.
def send_str(text: str):
    logging.debug(text)

# send json data.
# you can send any object as json using this function
def send_json(dat: object):
    s = json.dumps(dat)
    send_str(s)

