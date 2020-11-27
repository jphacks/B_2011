// const { ipcRenderer } = require('electron')
// ipcRenderer.send('take_photo', 'get_user_info');
// ipcRenderer.on('take_photo', (event, data) => {
//     document.getElementById('exam_id').innerText = data.exam_id
//     document.getElementById('user_id').innerText = data.user_id
//     console.log(data.exam_id);
// });

var enabled = true;
var WebCamera = require("webcamjs");
var fs = require('fs')
const path = require('path');

WebCamera.set({
    width: 640,
    height: 480,
    dest_width: 640,
    dest_height: 480,
    crop_width: 640,
    crop_height: 480
});

WebCamera.attach('#camera_screen');
console.log("The camera has been started");

function processBase64Image(dataString) {
    var matches = dataString.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/),response = {};

    if (matches.length !== 3) {
        return new Error('Invalid input string');
    }

    response.type = matches[1];
    response.data = new Buffer.from(matches[2], 'base64');

    return response;
}

document.getElementById("take_photo").addEventListener('click', () => {
    if(enabled) {
        WebCamera.snap(data_uri => {
            var imageBuffer = processBase64Image(data_uri);
            fs.writeFile(path.join(__dirname, '../../../img/user_valid.png'), imageBuffer.data, function(err) {
                if(err) {
                    console.log("Cannot save image");
                } else {
                    alert("写真撮影ができました。");
                    WebCamera.reset();
                    // Proceed to next page
                    document.location.href = "record_sound.html"
                }
            });
        });
    } else {
        console.log("Please enable the camera");
    }
}, false);
