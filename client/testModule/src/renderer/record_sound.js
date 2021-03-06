const fs = require('fs')
const record = document.getElementById('record')
const soundClips = document.querySelector('.sound-clips');

let vowels = ['a', 'i', 'u', 'e', 'o']
let vowel_index = 0;

const change_vowel = (vowel) => {
    const voice_type_element = document.getElementById('voice_type')
    switch(vowel) {
        case 'a':
            voice_type_element.innerText = 'あ'
            break;
        case 'i':
            voice_type_element.innerText = 'い'
            break;
        case 'u':
            voice_type_element.innerText = 'う'
            break;
        case 'e':
            voice_type_element.innerText = 'え'
            break;
        case 'o':
            voice_type_element.innerText = 'お'
            break;
    }
}


// if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
//     console.log('getUserMedia supported.');
//     navigator.mediaDevices.getUserMedia (
//        // constraints - only audio needed for this app
//        {
//           audio: true
//        })
 
//        // Success callback
//        .then(function(stream) {
//             const mediaRecorder = new MediaRecorder(stream);

//             record.onclick = function() {
//                 mediaRecorder.start();
//                 console.log(mediaRecorder.state);
//                 console.log("recorder started");
//                 record.style.background = "red";
//                 record.innerText = "録音中..."
//                 record.style.color = "#fff"
//                 record.disabled = true
//                 setTimeout(() => {
//                     mediaRecorder.stop();
//                     console.log(mediaRecorder.state);
//                     console.log("recorder stopped");
//                     record.style.background = "";
//                     record.style.color = "";
//                     record.innerText = "録音"
//                     record.disabled = false
//                     vowel_index += 1
//                     if (vowel_index == 5) {
//                         document.getElementById('voice_type_box').style.display = 'none'
//                         document.getElementById('record').style.display = 'none'
//                         document.getElementById('next_page').onclick = () => {
//                             document.location.href = "exam_prep.html"
//                         }
//                         document.getElementById('next_page').style.display = 'block'
//                     }
//                     change_vowel(vowels[vowel_index])
//                 }, 5500)
//             }

//             let chunks = [];
//             mediaRecorder.ondataavailable = function(e) {
//                 chunks.push(e.data);
//             }

//             mediaRecorder.onstop = function(e) {
//                 console.log("recorder stopped");
              
//                 const clipContainer = document.createElement('article');
//                 const clipLabel = document.createElement('span');
//                 const audio = document.createElement('audio');
//                 const clear = document.createElement('div');
                         
//                 clipContainer.classList.add('clip');
//                 audio.setAttribute('controls', '');
//                 audio.style.width = '200px'
//                 audio.style.float = 'right'
//                 audio.style.height = '50px'
//                 audio.style.verticalAlign = 'middle'
//                 clipLabel.style.float = 'left'
//                 clipLabel.style.fontSize = '30px'
//                 clipLabel.style.color = '#087fe9ff'
//                 clipLabel.style.backgroundColor = '#fff'
//                 clipLabel.style.padding = '3px 10px'
//                 clear.style.clear = 'both'
//                 clear.style.marginBottom = '10px'
                
//                 switch(vowels[vowel_index-1]) {
//                     case 'a':
//                         clipLabel.innerHTML = 'あ'
//                         break;
//                     case 'i':
//                         clipLabel.innerHTML = 'い'
//                         break;
//                     case 'u':
//                         clipLabel.innerHTML = 'う'
//                         break;
//                     case 'e':
//                         clipLabel.innerHTML = 'え'
//                         break;
//                     case 'o':
//                         clipLabel.innerHTML = 'お'
//                         break;
//                 }

//                 clipContainer.appendChild(clipLabel);
//                 clipContainer.appendChild(audio);
//                 clipContainer.appendChild(clear);
//                 soundClips.appendChild(clipContainer);
              
//                 const blob = new Blob(chunks, { 'type' : 'audio/wav; codecs=opus' });
//                 chunks = [];
//                 const audioURL = window.URL.createObjectURL(blob);
//                 audio.src = audioURL;
                
//                 blob.arrayBuffer().then(buffer => {
//                     fs.writeFileSync('python_code/voice/wav/0_' + vowels[vowel_index-1] + '.wav', Buffer.from(buffer))
//                 })
//             }
         
//        })
 
//        // Error callback
//        .catch(function(err) {
//           console.log('The following getUserMedia error occured: ' + err);
//        }
//     );
// } else {
//     console.log('getUserMedia not supported on your browser!');
// }

const AudioRecorder = require('node-audiorecorder');

const options = {
    program: `rec`,     // Which program to use, either `arecord`, `rec`, or `sox`.
    device: null,       // Recording device to use, e.g. `hw:1,0`
  
    bits: 16,           // Sample size. (only for `rec` and `sox`)
    channels: 1,        // Channel count.
    encoding: `signed-integer`,  // Encoding type. (only for `rec` and `sox`)
    format: `S16_LE`,   // Encoding type. (only for `arecord`)
    rate: 16000,        // Sample rate.
    type: `wav`,        // Format type.
  
    // Following options only available when using `rec` or `sox`.
    // silence: 2,         // Duration of silence in seconds before it stops recording.
    // thresholdStart: 0.5,  // Silence threshold to start recording.
    // thresholdStop: 0.5,   // Silence threshold to stop recording.
    // keepSilence: true   // Keep the silence in the recording.
};

const logger = console;

let audioRecorder = new AudioRecorder(options, logger);

record.onclick = function() {
    vowel = vowels[vowel_index]
    const fileName = 'python_code/voice/wav/0_' + vowel + '.wav'
    const fileStream = fs.createWriteStream(fileName, { encoding: 'binary' });
    audioRecorder.start().stream().pipe(fileStream);

    audioRecorder.stream().on('close', function(code) {
        console.warn('Recording closed. Exit code: ', code);
    });
    audioRecorder.stream().on('end', function() {
        console.warn('Recording ended.');
    });
    audioRecorder.stream().on('error', function() {
        console.warn('Recording error.');
    });

    console.log("Recording started");
    record.style.background = "red";
    record.innerText = "録音中..."
    record.style.color = "#fff"
    record.disabled = true
    setTimeout(() => {
        audioRecorder.stop();
        record.style.background = "";
        record.style.color = "";
        record.innerText = "録音"
        record.disabled = false
        vowel_index += 1
        if (vowel_index == 5) {
            document.getElementById('voice_type_box').style.display = 'none'
            document.getElementById('record').style.display = 'none'
            document.getElementById('next_page').onclick = () => {
                document.location.href = "exam_prep.html"
            }
            document.getElementById('next_page').style.display = 'block'
        }
        change_vowel(vowels[vowel_index])
    }, 6000)
}