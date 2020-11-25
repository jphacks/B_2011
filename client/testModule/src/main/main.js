// require('update-electron-app')({
//     logger: require('electron-log')
// })

if (require('electron-squirrel-startup')) return;

const { app, BrowserWindow, ipcMain } = require('electron')
const url = require('url')
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

// app.whenReady().then(createWindow)

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

let exam_id = '';
let user_id = '';
ipcMain.on('asynchronous-message', (event, arg) => {
    console.log("Exam ID: ", arg.exam_id);
    console.log("User ID: ", arg.user_id);
    exam_id = arg.exam_id;
    user_id = arg.user_id;
    helper.send_json(user_id, exam_id, "user_log", "User logged in", "User has logged in from desktop App.")
});

ipcMain.on('take_photo', (event, data) => {
    event.reply('take_photo', {exam_id: exam_id, user_id: user_id});
});