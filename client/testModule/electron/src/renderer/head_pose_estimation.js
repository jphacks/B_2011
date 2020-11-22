const net = require('net')
const request = require('request');

if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
	console.log("enumerateDevices() not supported.");
}

// List cameras
navigator.mediaDevices.enumerateDevices().then(devices => {
    const sel = document.getElementById('camera-device-id');
    devices.forEach(function(device) {
        console.log(device.kind + ": " + device.label + " id = " + device.deviceId);
        if (device.kind == 'videoinput') {
            var opt = document.createElement('option');
            opt.appendChild(document.createTextNode(device.label));
            opt.value = device.deviceId;
            sel.appendChild(opt);
        }
    });
}).catch(err => console.log(err.name + ": " + err.message));

const myDeviceId = document.getElementById('camera-device-id').value;

navigator.mediaDevices.getUserMedia({
    video: {deviceId: myDeviceId},
    audio: false,
}).then(stream => {
    const video = document.getElementById('video');
    video.srcObject = stream;
    video.play();
}).catch(error => alert('Cannot connect to camera: ' + error));

const faceapi = require('face-api.js')

faceapi.env.monkeyPatch({
    Canvas: HTMLCanvasElement,
    Image: HTMLImageElement,
    ImageData: ImageData,
    Video: HTMLVideoElement,
    createCanvasElement: () => document.createElement('canvas'),
    createImageElement: () => document.createElement('img')
})

faceapi.nets.tinyFaceDetector.loadFromUri('models/weights')
faceapi.nets.faceLandmark68TinyNet.loadFromUri('models/weights')

const cv = require('./opencv.js')

let yaw_left_count = 0;
let yaw_right_count = 0;
detect();
async function detect() {
    requestAnimationFrame(detect);

    //  webカメラの映像から顔認識を行う
    const useTinyModel = true;
    const detection = await faceapi
        .detectSingleFace(
            video,
            new faceapi.TinyFaceDetectorOptions({
                inputSize: 160,
            })
        )
        .withFaceLandmarks(useTinyModel);

    if (!detection) {
        return;
    }

    // 認識データをリサイズ
    const resizedDetection = faceapi.resizeResults(detection, {
        width: video.width,
        height: video.height,
    });

    // ランドマークをキャンバスに描画
    const canvas = document.getElementById('canvas1');
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    faceapi.draw.drawFaceLandmarks(canvas, resizedDetection);

    // 以後使用するランドマーク座標
    const landmarks = resizedDetection.landmarks;
    const nose = landmarks.getNose()[3];
    const leftEye = landmarks.getLeftEye()[0];
    const rightEye = landmarks.getRightEye()[3];
    const jaw = landmarks.getJawOutline()[8];
    const leftMouth = landmarks.getMouth()[0];
    const rightMouth = landmarks.getMouth()[6];
    const leftOutline = landmarks.getJawOutline()[0];
    const rightOutline = landmarks.getJawOutline()[16];
    
    const { success, imagePoints, cameraMatrix, distCoeffs, rvec, tvec } = solve(nose, leftEye, rightEye, jaw, leftMouth, rightMouth, leftOutline, rightOutline)
    const { yaw, pitch, roll } = headpose(rvec, tvec, cameraMatrix, distCoeffs, imagePoints)
    // console.log(yaw, pitch, roll)
    if (yaw <= -45) {
        yaw_left_count += 1
    } else if (yaw >= 45) {
        yaw_right_count += 1
    }
    if (yaw_left_count > 20) {
        const myNotification = new Notification('Head position alert', {
            body: 'You are looking to the left. Please focus on the screen.'
        })
        var options = {
            uri: "http://demo.ben.hongo.wide.ad.jp:8000/api/message/list",
            headers: {
              "Content-type": "application/json",
            },
            json: [{
              "examinee_id": "ee6b3ea2-8858-4cc3-a413-3dde08055225",
              "exam_id": "911f6e61-e061-4be9-9f25-246e1fb16207",
              "module_name": 'electron_head_position',
              'alert': 'True',
              'description': 'User is looking to the left',
              'content': 'yaw: ' + String(yaw)
            }]
        };
        request.post(options, function(error, response, body){});
        yaw_left_count = 0
    } else if (yaw_right_count > 20) {
        const myNotification = new Notification('Head position alert', {
            body: 'You are looking to the right. Please focus on the screen.'
        })
        var options = {
            uri: "http://demo.ben.hongo.wide.ad.jp:8000/api/message/list",
            headers: {
              "Content-type": "application/json",
            },
            json: [{
              "examinee_id": "ee6b3ea2-8858-4cc3-a413-3dde08055225",
              "exam_id": "911f6e61-e061-4be9-9f25-246e1fb16207",
              "module_name": 'electron_head_position',
              'alert': 'True',
              'description': 'User is looking to the right',
              'content': 'yaw: ' + String(yaw)
            }]
        };
        request.post(options, function(error, response, body){});
        yaw_right_count = 0
    }
}

// capture model points
const detectPoints = [
    // nose
    ...[0.0, 0.0, 0.0],
    // jaw
    ...[0, -330, -65],
    // left eye
    ...[-240, 170, -135],
    // right eye
    ...[240, 170, -135],
    // left mouth
    ...[-150, -150, -125],
    // right mouth
    ...[150, -150, -125],
    // left outline
    ...[-480, 170, -340],
    // right outline
    ...[480, 170, -340],
];

function solve(nose, leftEye, rightEye, jaw, leftMouth, rightMouth, leftOutline, rightOutline) {
    const rows = detectPoints.length / 3;
    const modelPoints = cv.matFromArray(rows, 3, cv.CV_64FC1, detectPoints);
    // camera matrix
    const size = {
        width: 640,
        height: 480,
    };
    const center = [size.width / 2, size.height / 2];
    const cameraMatrix = cv.matFromArray(3, 3, cv.CV_64FC1, [
        ...[size.width, 0, center[0]],
        ...[0, size.width, center[1]],
        ...[0, 0, 1],
    ]);

    // image matrix
    const imagePoints = cv.Mat.zeros(rows, 2, cv.CV_64FC1);
    const distCoeffs = cv.Mat.zeros(4, 1, cv.CV_64FC1);
    const rvec = new cv.Mat({ width: 1, height: 3 }, cv.CV_64FC1);
    const tvec = new cv.Mat({ width: 1, height: 3 }, cv.CV_64FC1);

    const destructured_array =  [nose.x, nose.y, jaw.x, jaw.y, leftEye.x, leftEye.y, rightEye.x, rightEye.y, leftMouth.x, leftMouth.y, rightMouth.x, rightMouth.y, leftOutline.x, leftOutline.y, rightOutline.x, rightOutline.y]
    destructured_array.map((v, i) => {
        imagePoints.data64F[i] = v;
    });

    // 移動ベクトルと回転ベクトルの初期値を与えることで推測速度の向上をはかる
    tvec.data64F[0] = -100;
    tvec.data64F[1] = 100;
    tvec.data64F[2] = 1000;
    const distToLeftEyeX = Math.abs(leftEye[0] - nose[0]);
    const distToRightEyeX = Math.abs(rightEye[0] - nose[0]);
    if (distToLeftEyeX < distToRightEyeX) {
        // 左向き
        rvec.data64F[0] = -1.0;
        rvec.data64F[1] = -0.75;
        rvec.data64F[2] = -3.0;
    } else {
        // 右向き
        rvec.data64F[0] = 1.0;
        rvec.data64F[1] = -0.75;
        rvec.data64F[2] = -3.0;
    }

    const success = cv.solvePnP(
        modelPoints,
        imagePoints,
        cameraMatrix,
        distCoeffs,
        rvec,
        tvec,
        true
    );

    return {
        success,
        imagePoints,
        cameraMatrix,
        distCoeffs,
        rvec, // 回転ベクトル
        tvec, // 移動ベクトル
    };
}

function headpose(rvec, tvec, cameraMatrix, distCoeffs, imagePoints) {
    const noseEndPoint2DZ = new cv.Mat();
    const noseEndPoint2DY = new cv.Mat();
    const noseEndPoint2DX = new cv.Mat();

    const pointZ = cv.matFromArray(1, 3, cv.CV_64FC1, [0.0, 0.0, 500.0]);
    const pointY = cv.matFromArray(1, 3, cv.CV_64FC1, [0.0, 500.0, 0.0]);
    const pointX = cv.matFromArray(1, 3, cv.CV_64FC1, [500.0, 0.0, 0.0]);
    const jaco = new cv.Mat();

    cv.projectPoints(
        pointZ,
        rvec,
        tvec,
        cameraMatrix,
        distCoeffs,
        noseEndPoint2DZ,
        jaco
    );
    cv.projectPoints(
        pointY,
        rvec,
        tvec,
        cameraMatrix,
        distCoeffs,
        noseEndPoint2DY,
        jaco
    );
    cv.projectPoints(
        pointX,
        rvec,
        tvec,
        cameraMatrix,
        distCoeffs,
        noseEndPoint2DX,
        jaco
    );

    const canvas2 = document.getElementById('canvas2');
    const context = canvas2.getContext('2d');

    const position = {
        nose: {
            x: imagePoints.data64F[0],
            y: imagePoints.data64F[1],
        },
        x: {
            x: noseEndPoint2DX.data64F[0],
            y: noseEndPoint2DX.data64F[1],
        },
        y: {
            x: noseEndPoint2DY.data64F[0],
            y: noseEndPoint2DY.data64F[1],
        },
        z: {
            x: noseEndPoint2DZ.data64F[0],
            y: noseEndPoint2DZ.data64F[1],
        },
    };

    context.clearRect(0, 0, canvas2.width, canvas2.height);

    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = 'rgb(255, 0, 0)';
    context.moveTo(position.nose.x, position.nose.y);
    context.lineTo(position.z.x, position.z.y);
    context.stroke();
    context.closePath();

    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = 'rgb(0, 0, 255)';
    context.moveTo(position.nose.x, position.nose.y);
    context.lineTo(position.x.x, position.x.y);
    context.stroke();
    context.closePath();

    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = 'rgb(0, 255, 0)';
    context.moveTo(position.nose.x, position.nose.y);
    context.lineTo(position.y.x, position.y.y);
    context.stroke();
    context.closePath();

    const rmat = new cv.Mat();
    cv.Rodrigues(rvec, rmat);

    const projectMat = cv.Mat.zeros(3, 4, cv.CV_64FC1);
    projectMat.data64F[0] = rmat.data64F[0];
    projectMat.data64F[1] = rmat.data64F[1];
    projectMat.data64F[2] = rmat.data64F[2];
    projectMat.data64F[4] = rmat.data64F[3];
    projectMat.data64F[5] = rmat.data64F[4];
    projectMat.data64F[6] = rmat.data64F[5];
    projectMat.data64F[8] = rmat.data64F[6];
    projectMat.data64F[9] = rmat.data64F[7];
    projectMat.data64F[10] = rmat.data64F[8];

    const cmat = new cv.Mat();
    const rotmat = new cv.Mat();
    const travec = new cv.Mat();
    const rotmatX = new cv.Mat();
    const rotmatY = new cv.Mat();
    const rotmatZ = new cv.Mat();
    const eulerAngles = new cv.Mat();

    cv.decomposeProjectionMatrix(
        projectMat,
        cmat,
        rotmat,
        travec,
        rotmatX,
        rotmatY,
        rotmatZ,
        eulerAngles // 顔の角度情報
    );

    return {
        yaw: eulerAngles.data64F[1],
        pitch: eulerAngles.data64F[0],
        roll: eulerAngles.data64F[2],
    };
}

function showNotification(title, body) {
    const notification = {
        title: title,
        body: body
    }
    new Notification(notification).show()
}

