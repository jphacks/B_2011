import sys
import os
# sys.path.append(os.path.abspath(".."))
import time
import face_recognition

#save examinee's photo as valid.png before exam starts
valid_uri = '../img/valid2.png'
sample_uri = '../img/sample.png'

while(True):
	#run validation once a second
	time.sleep(1)

	try:
		valid_image = face_recognition.load_image_file(valid_uri)
		sample_image = face_recognition.load_image_file(sample_uri)
	except:
		print('Image not valid')
		sys.stdout.flush()
		continue

	try:	
		valid_encoding = face_recognition.face_encodings(valid_image)[0]
		sample_encoding = face_recognition.face_encodings(sample_image)[0]
		result = face_recognition.compare_faces([valid_encoding], sample_encoding)[0]
		# for debug
		print('distance is ', result)
		sys.stdout.flush()
	except:
		description = 'any face cannot be detected'
		# helper.send_json(module_name, True, description, content)
		print(description)
		sys.stdout.flush()
		continue

	if result > 0.4:
		description = 'different person might be taking exam'
		# helper.send_json(module_name, True, description, content)
		print(description)
		sys.stdout.flush()
	else:
		description = 'examinee is on the chair'
	