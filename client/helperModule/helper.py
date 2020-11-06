import logging
import json

import pprint
# TODO: send string to server
# temporarily, use logging.debug

# send string data.
def send_str(text: str):
    logging.debug(text)

# send json data.
# you can send any object as json using this function
def send_json(  exam_id,
                tester_id,
                tester_name,
                examinee_id,
                module_name,
                alert,
                description,
                content
                ):
    d = {}
    d["exam_id"] = exam_id
    d["tester_id"] = tester_id
    d["tester_name"] = tester_name
    d["examinee_id"] = examinee_id
    d["module_name"] = module_name
    d["alert"] = alert
    d["description"] = description
    d["content"] = content 
    s = json.dumps(d)
    
    pprint.pprint(s)
    # logging.debug(s)
    # send_str(s)

