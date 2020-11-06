import logging
import json
import requests
import queue
import time
import sys
import os
sys.path.append(os.path.abspath('..'))
import main

server_url = "http://demo.ben.hongo.wide.ad.jp:8000/api/message/list"
que = queue.Queue() # thread safe
send_interval = 10 # [sec]
start = 0 # the time to clear the queue.

# load user id
# TODO : return the examinee_id
def load_userid():
    return main.examinee_id

def load_examid():
    return main.exam_id

# call first.
def init_time():
    global start
    start = time.time()

# 定期的にmain.pyから呼ばれる必要がある。
def time_passed():
    global start, send_interval, que
    now = time.time()
    if (now - start >= send_interval) and (que.qsize() > 0):
        send_json_to_server()
        que = queue.Queue()
        start = now

def send_json_to_server():
    global que, server_url
    list_que = list(que.queue) # dumpするときにlistに変換
    dumped_json = json.dumps(list_que)
    logging.debug(dumped_json)
    requests.post(
        url = server_url,
        data = dumped_json,
        headers={'Content-Type': 'application/json'}
    )

# push json data to queue
def push_to_queue(json_data):
    que.put(json_data)

# TODO : fix the alert from bool to string
def send_json(module_name: str, alert: bool, description: str = '', content: str = ''):
    user_id = load_userid()
    exam_id = load_examid()
    json_data = {
        "examinee_id" : user_id,
        "exam_id" : exam_id,
        "module_name" : module_name,
        "alert" : "True",
        "description" : description,
        "content" : content,
    }
    push_to_queue(json_data)
    
