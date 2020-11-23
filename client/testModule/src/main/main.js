if (require('electron-squirrel-startup')) return;
require('dotenv').config()

const { app, BrowserWindow, Notification, nativeImage } = require('electron')

const url = require('url')
const path = require('path')

app.setAppUserModelId("com.electron.satori")

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        },
        icon: nativeImage.createFromPath(path.join(__dirname, 'satori.png'))
    })

    // win.loadFile('index.html')
    // win.webContents.openDevTools()
    win.loadURL(url.format({
        pathname: path.join(__dirname, '../renderer/login.html'),
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
