if (require('electron-squirrel-startup')) return;

const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')

// app.disableHardwareAcceleration()

app.setAppUserModelId("com.electron.satori")

function createWindow() {
    const win = new BrowserWindow({
        width: 1080,
        minWidth: 680,
        height: 840,
        webPreferences: {
            nodeIntegration: true
        }
    })

    win.loadURL(path.join('file://', __dirname, '../renderer/login.html'))
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
let exam_id = '911f6e61-e061-4be9-9f25-246e1fb16207';
let user_id = '911f6e61-e061-4be9-9f25-246e1fb16207';

ipcMain.on('asynchronous-message', (event, arg) => {
    console.log("Exam ID: ", arg.exam_id);
    console.log("User ID: ", arg.user_id);
    exam_id = arg.exam_id;
    user_id = arg.user_id;
    send_json('user_log', 'User logged in', 'User has logged in from desktop App.')
});

// IPC with "take_photo.js"
ipcMain.on('take_photo', (event, data) => {
    // Send back the exam_id and user_id
    event.reply('take_photo', {exam_id: exam_id, user_id: user_id});
});

// IPC with "exam_prep.js"
ipcMain.on('exam_prep', (event, data) => {
    // Send back the exam_id and user_id
    event.reply('exam_prep', {exam_id: exam_id, user_id: user_id});
});

ipcMain.on('active_window', (event, data) => {
    console.log('[SERVER] active_window ', data.description)
    send_json('active_window', data.description, '')
});

ipcMain.on('clipboard', (event, data) => {
    console.log('[SERVER] clipboard ', data.description)
    send_json('clipboard', data.description, '')
});

ipcMain.on('head_pose_estimation', (event, data) => {
    console.log('[SERVER] head_pose_estimation ', data.description)
    send_json('head_pose_estimation', data.description, '')
});

// Connect with server
const send_json = (module_name, description, content) => {
    
    const http = require('http')

    const data = JSON.stringify([{
        "examinee_id": user_id,
        "exam_id": exam_id,
        "module_name": module_name,
        "alert": "True",
        "description": description,
        "content": content,
    }])

    const options = {
        hostname: 'demo.ben.hongo.wide.ad.jp',
        port: 8000,
        path: '/api/message/list',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': data.length
        }
    }

    const req = http.request(options, res => {
        console.log(`statusCode: ${res.statusCode}`)
      
        res.on('data', d => {
            process.stdout.write(d)
        })
    })

    req.on('error', error => {
        console.error(error)
    })

    req.write(data)
    req.end()
    
}
