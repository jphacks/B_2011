import logging
import json
import requests
import sys
import os
sys.path.append(os.path.abspath('..'))
import main
import websocket

server_url = "http://demo.ben.hongo.wide.ad.jp:8000/api/message/list"
websocket.enableTrace(True)

ws = None
exam_id = ''
examinee_id = ''

def on_message(ws, message):
    logging.debug(message)

def on_error(ws, error):
    logging.debug('websocket connection closed on error)')

def on_close(ws):
    logging.debug('websocket connection closed')

ws = None
# TODO : fix the alert from bool to string
def send_json(module_name: str, alert: bool, description: str = '', content: str = ''):
    global exam_id, examinee_id, ws
    logging.debug(exam_id)
    json_data = {
        "examinee_id" : examinee_id,
        "exam_id" : exam_id,
        "module_name" : module_name,
        "alert" : "True",
        "description" : description,
        "content" : content,
    }
    json_data = json.dumps(json_data)
    logging.debug(json_data)
    ws.send(json_data)

#start websocket connection to server    
def run_websocket():
    global examinee_id, ws
    logging.debug(examinee_id)
    ws = websocket.WebSocketApp('ws://localhost:8000/ws/examinee/'+ examinee_id,
							  on_message = on_message,
							  on_error = on_error,
							  on_close = on_close)
    ws.run_forever()
