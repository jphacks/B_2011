if (require('electron-squirrel-startup')) return;

const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const helper = require('../helper')

app.disableHardwareAcceleration()

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
let exam_id = '';
let user_id = '';
ipcMain.on('asynchronous-message', (event, arg) => {
    console.log("Exam ID: ", arg.exam_id);
    console.log("User ID: ", arg.user_id);
    exam_id = arg.exam_id;
    user_id = arg.user_id;

    // Send JSON to API server
    helper.send_json(user_id, exam_id, "user_log", "User logged in", "User has logged in from desktop App.")
});

// IPC with "take_photo.js"
ipcMain.on('take_photo', (event, data) => {
    // Send back the exam_id and user_id
    event.reply('take_photo', {exam_id: exam_id, user_id: user_id});
});