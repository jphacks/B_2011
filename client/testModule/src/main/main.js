if (require('electron-squirrel-startup')) return;

const { app, BrowserWindow, ipcMain, Notification, screen } = require('electron')
const WebSocket = require('ws')
const path = require('path')

// app.disableHardwareAcceleration()

app.setAppUserModelId("com.electron.satori")

let win;

function createWindow() {
    win = new BrowserWindow({
        width: 1080,
        minWidth: 680,
        height: 840,
        webPreferences: {
            nodeIntegration: true
        }
    })

    win.loadURL(path.join('file://', __dirname, '../renderer/login.html'))
}

function showNotification_dualscreen() {
    const notification = {
        title: 'Second screen detected.',
        body: 'You cannot use second screen.'
    }
    new Notification(notification).show()
}

function detect_dual_screen() {
    setInterval(function() {
        let displays = screen.getAllDisplays()
        let externalDisplay = displays.find((display) => {
            return display.bounds.x !== 0 || display.bounds.y !== 0
        })
        if (externalDisplay) {
            showNotification_dualscreen();
            console.log('second screen detected!');
            send_json('second_screen', 2 ,'Second screen detected', '')
        }
    }, 2000);
}

app.on('ready', () => {
    createWindow()
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})

// 
// IPC between renderer processes
//

// IPC with "login.js"
let exam_id = '072d2d97-e528-4aa3-9e24-6aa71b87b98a';
let user_id = '7cfc21fb-b096-4005-a100-1dd55e719903';

ipcMain.on('asynchronous-message', (event, arg) => {
    console.log("Exam ID: ", arg.exam_id);
    console.log("User ID: ", arg.user_id);
    exam_id = arg.exam_id;
    user_id = arg.user_id;
    send_json('user_log', 'User logged in', 'User has logged in from desktop App.')
});

ipcMain.on('dual_display_detect', (event, data) => {
    detect_dual_screen();
});

// IPC with "take_photo.js"
ipcMain.on('take_photo', (event, data) => {
    // Send back the exam_id and user_id
    event.reply('take_photo', { exam_id: exam_id, user_id: user_id });
});

// IPC with "exam_prep.js"
ipcMain.on('exam_prep', (event, data) => {
    // Send back the exam_id and user_id
    event.reply('exam_prep', { exam_id: exam_id, user_id: user_id });
});

ipcMain.on('exam', (event, data) => {
    // Send back the exam_id and user_id
    event.reply('exam', { exam_id: exam_id, user_id: user_id });
});

ipcMain.on('active_window', (event, data) => {
    console.log('[SERVER] active_window ', data.alert, data.description)
    send_json('active_window', data.alert, data.description, '')
});

ipcMain.on('clipboard', (event, data) => {
    console.log('[SERVER] clipboard ', data.alert, data.description)
    send_json('clipboard', data.alert, data.description, '')
});

ipcMain.on('head_pose_estimation', (event, data) => {
    console.log('[SERVER] head_pose_estimation ', data.alert, data.description)
    send_json('head_pose_estimation', data.alert, data.description, '')
});

ipcMain.on('face_recognition', (event, data) => {
    console.log('[SERVER] face_recognition ', data.alert, data.description)
    send_json('face_recognition', data.alert, data.description, '')
});

ipcMain.on('ssh_process_name', (_, data) => {
    console.log('[SERVER] ssh_process_name ', data.alert, data.description)
    send_json('ssh_process_name', data.alert, data.description, '')
});

ipcMain.on('ssh_network_traffic', (_, data) => {
    console.log('[SERVER] ssh_network_traffic ', data.alert, data.description)
    send_json('ssh_network_traffic', data.alert, data.description, '')
})

ipcMain.on('exam_finished', (event, data) => {
    app.quit()
});

// Connect with server
var connection = new WebSocket(
    "ws://ben.hongo.wide.ad.jp:8000/ws/examinee/" + exam_id
);

async function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
};

connection.onopen = function() {
    console.log("websocket connection established");
};

connection.onerror = function() {
    console.log("websocket connection closed on error");
    connection = new WebSocket(
        "ws://ben.hongo.wide.ad.jp:8000/ws/examinee/" + exam_id
    );
};

connection.onmessage = function(e) {
    console.log(e.data);
    const notification = {
        title: '試験監督からの新着メッセージ',
        body: e.data
    }
    new Notification(notification).show()
    win.webContents.send('proctor-message', e.data)
};

connection.onclose = function() {
    console.log("websocket connection closed");
    connection = new WebSocket(
        "ws://ben.hongo.wide.ad.jp:8000/ws/examinee/" + exam_id
    );
};

async function send_json(module_name, alert, description, content) {
    let data = {
        examinee_id: user_id,
        exam_id: exam_id,
        module_name: module_name,
        alert: alert,
        description: description,
        content: content,
    };
    let json_data = JSON.stringify(data);
    while (true) {
        if (connection.readyState === 1) {
            connection.send(json_data);
            break;
        } else {
            await sleep(1000);
        };
    };
};
