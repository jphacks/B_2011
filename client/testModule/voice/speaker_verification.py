from pydub import AudioSegment
import speaker_verification_toolkit.tools as svt
import numpy as np
import os

# memo : svt.find_nearest_voice_data()の引数は、numpyのarray形式。
dir_path = './dialogue-demo/record_ATR/wav'
path1 = os.path.join(dir_path, 's1_b03.wav')
path2 = os.path.join(dir_path, 's2_b03.wav')
path3 = os.path.join(dir_path, 's3_b03.wav')
path4 = os.path.join(dir_path, 's4_b03.wav')
voice_sample_path = os.path.join(dir_path, 's3_b04.wav')
path_list = [path1, path2, path3, path4]

sound = []
for i in range(4):
    sound.append(AudioSegment.from_file(path_list[i], 'wav'))

data = []
for i in range(4):
    data.append(np.array(sound[i].get_array_of_samples()))

voice_sample = AudioSegment.from_file(voice_sample_path, "wav")
data_sample = np.array(voice_sample.get_array_of_samples())

print(svt.find_nearest_voice_data(data, data_sample))