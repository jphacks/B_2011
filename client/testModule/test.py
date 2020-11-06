import sys
import os
sys.path.append(os.path.abspath(".."))
from helperModule import helper

def hoge():
    helper.send_str("testing...")

