import sys
import os
sys.path.append(os.path.abspath(".."))
import cv2
from datetime import datetime
import time

cap = cv2.VideoCapture(0)

def sampling_pics():
	prev_time=time.time()
	path = './img/sample.png'
	while True:
		current_time = time.time()
		if current_time - prev_time > 1:
			ret, frame = cap.read()
			cv2.imwrite(path, frame)
			prev_time = current_time


