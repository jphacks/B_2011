from socketserver import TCPServer, BaseRequestHandler
import json
import subprocess
import threading
from helperModule import helper

class EchoHandler(BaseRequestHandler):
    def handle(self):
        msg_b = self.request.recv(1024)
        msg_s = msg_b.decode('utf-8')
        dat = json.loads(msg_s)
        if dat != {}:
            helper.send_json(
                module_name=(dat['module'] if 'module' in dat else ''),
                alert='True',
                description=(dat['msg'] if 'msg' in dat else ''),
                content=''
            )

def createServer():
    address = ('localhost', 54321)
    TCPServer.allow_reuse_address = True
    # create tcp server
    with TCPServer(address, EchoHandler) as server:
        server.serve_forever()

def startElectron():
    subprocess.call('npm start', cwd=r'./testModule/electron', shell=True)

