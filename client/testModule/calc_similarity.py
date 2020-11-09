import sys
import os
sys.path.append(os.path.abspath(".."))
import time
from testModule import face_recognition
from helperModule import helper

def calc_similarity():
	#save examinee's photo as valid.png before exam starts
	valid_uri = './img/valid.png'
	sample_uri = './img/sample.png'

	module_name = "face_validation"
	content = ""

	while(True):
		#run validation once a second
		time.sleep(1)

		valid_image = face_recognition.load_image_file(valid_uri)
		sample_image = face_recognition.load_image_file(sample_uri)

		try:	
			valid_encoding = face_recognition.face_encodings(valid_image)[0]
			sample_encoding = face_recognition.face_encodings(sample_image)[0]
			result = face_recognition.compare_faces([valid_encoding], sample_encoding)[0]
			#for debug
			#print('distance is',result)
		except:
			description = 'any face cannot be detected'
			helper.send_json(module_name, True, description, content)
			continue

		if result > 0.4:
			description = 'different person might be taking exam'
			helper.send_json(module_name, True, description, content)
		else:
			description = 'examinee is on the chair'
