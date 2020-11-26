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


if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    console.log('getUserMedia supported.');
    navigator.mediaDevices.getUserMedia (
       // constraints - only audio needed for this app
       {
          audio: true
       })
 
       // Success callback
       .then(function(stream) {
            const mediaRecorder = new MediaRecorder(stream);

            record.onclick = function() {
                mediaRecorder.start();
                console.log(mediaRecorder.state);
                console.log("recorder started");
                record.style.background = "red";
                record.style.color = "black";
                record.innerText = "STOP"
                setTimeout(() => {
                    mediaRecorder.stop();
                    console.log(mediaRecorder.state);
                    console.log("recorder stopped");
                    record.style.background = "";
                    record.style.color = "";
                    record.innerText = "START"
                    vowel_index += 1
                    if (vowel_index == 5) {
                        document.location.href = "exam_prep.html"
                    }
                    change_vowel(vowels[vowel_index])
                }, 5000)
            }

            let chunks = [];
            mediaRecorder.ondataavailable = function(e) {
                chunks.push(e.data);
            }

            mediaRecorder.onstop = function(e) {
                console.log("recorder stopped");
              
                const clipContainer = document.createElement('article');
                const clipLabel = document.createElement('p');
                const audio = document.createElement('audio');
                const deleteButton = document.createElement('button');
                         
                clipContainer.classList.add('clip');
                audio.setAttribute('controls', '');
                deleteButton.innerHTML = "Delete";
                clipLabel.innerHTML = vowels[vowel_index-1];
              
                clipContainer.appendChild(audio);
                clipContainer.appendChild(clipLabel);
                clipContainer.appendChild(deleteButton);
                soundClips.appendChild(clipContainer);
              
                const blob = new Blob(chunks, { 'type' : 'audio/wav; codecs=opus' });
                chunks = [];
                const audioURL = window.URL.createObjectURL(blob);
                audio.src = audioURL;
                
                blob.arrayBuffer().then(buffer => {
                    fs.writeFileSync('voice/0_' + vowels[vowel_index-1] + '.wav', Buffer.from(buffer))
                })

                deleteButton.onclick = function(e) {
                  let evtTgt = e.target;
                  evtTgt.parentNode.parentNode.removeChild(evtTgt.parentNode);
                }
            }
         
       })
 
       // Error callback
       .catch(function(err) {
          console.log('The following getUserMedia error occured: ' + err);
       }
    );
} else {
    console.log('getUserMedia not supported on your browser!');
}