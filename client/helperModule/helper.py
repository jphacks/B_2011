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

# call first.
def init_time():
    start = time.time()

# 定期的にmain.pyから呼ばれる必要がある。
def time_passed():
    now = time.time()
    if (now - start >= send_interval) and (que.qsize() > 0):
        send_json_to_server()
        que = queue.Queue()
        start = now

def send_json_to_server():
    que = list(que.queue) # dumpするときにlistに変換
    dumped_json = json.dumps(que)
    requests.get(
        url = server_url,
        params = dumped_json
    )

# push json data to queue
def push_to_queue(json_data):
    que.put(json_data)

# send json data.
# you can send any object as json using this function
def send_json(module_name: str, alert: bool, description: str = ''):
    user_id = load_userid()
    json_data = {
        "examinee_id" : user_id,
        "module_name" : module_name,
        "alert" : alert,
        "description" : description
    }
    push_to_queue(json_data)

