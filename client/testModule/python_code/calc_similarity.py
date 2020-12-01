import sys
import os
# sys.path.append(os.path.abspath(".."))
import time
import face_recognition
import json

#save examinee's photo as valid.png before exam starts
valid_uri = '../img/user_valid.png'
sample_uri = '../img/sample.png'
counter = 0

while(True):
	#run validation once a second
	time.sleep(1)

	try:
		valid_image = face_recognition.load_image_file(valid_uri)
		sample_image = face_recognition.load_image_file(sample_uri)
	except:
		print(json.dumps({ "module" : "face_recognition" ,"alert": 1, "description": "Image not valid" }))
		sys.stdout.flush()
		continue

	try:	
		valid_encoding = face_recognition.face_encodings(valid_image)[0]
		sample_encoding = face_recognition.face_encodings(sample_image)[0]
		result = face_recognition.compare_faces([valid_encoding], sample_encoding)[0]
		# for debug
		# print('distance is ', result)
		# sys.stdout.flush()
		counter += 1
		if counter == 10:
			print(json.dumps({ "module" : "face_recognition" ,"alert": 0, "description": "normal" }))
			sys.stdout.flush()
			counter = 0
	except:
		description = 'any face cannot be detected'
		# helper.send_json(module_name, True, description, content)
		print(json.dumps({ "module" : "face_recognition" ,"alert": 1, "description": description }))
		sys.stdout.flush()
		continue

	if result > 0.4:
		description = 'different person might be taking exam'
		# helper.send_json(module_name, True, description, content)
		print(json.dumps({ "module" : "face_recognition" ,"alert": 1, "description": description }))
		sys.stdout.flush()
	else:
		description = 'examinee is on the chair'
	