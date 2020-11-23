// if (require('electron-squirrel-startup')) return;

const { app, BrowserWindow, Notification, nativeImage, ipcMain } = require('electron')

const url = require('url')
const path = require('path')

app.setAppUserModelId("com.electron.satori")

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    })

    win.loadURL(url.format({
        pathname: path.join(__dirname, '..' , 'renderer/login.html'),
        protocol: 'file:',
        slashes: true
    }))
}

function showNotification(title, body, module) {
    console.log("[notification] " + title + ' ' +  body)
    const notification = {
        title: title,
        body: body,
        icon: nativeImage.createFromPath(path.join(__dirname, 'satori.png'))
    }
    new Notification(notification).show()
}

app.whenReady().then(createWindow)

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

// let exam_id = '';
// let user_id = '';
// ipcMain.on('asynchronous-message', (event, arg) => {
//     console.log("Exam ID: ", arg.exam_id);
//     console.log("User ID: ", arg.user_id);
//     exam_id = arg.exam_id;
//     user_id = arg.user_id;
// });

// ipcMain.on('take_photo', (event, data) => {
//     event.reply('take_photo', {exam_id: exam_id, user_id: user_id});
// });