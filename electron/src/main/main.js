if (require('electron-squirrel-startup')) return;

const { app, BrowserWindow, Notification } = require('electron')
const clipboardy = require('clipboardy');
const activeWin = require('active-win');
const url = require('url')
const path = require('path')

let previous_clipboard = clipboardy.readSync();
let previous_active_app_title =  (async () => {
    active_app_title = (await activeWin()).title;
})();
const clipboard_interval = setInterval(function() {
    const current_clipboard = clipboardy.readSync()
	if (current_clipboard !== previous_clipboard) {
        previous_clipboard = current_clipboard
        showNotification('Copied to Clipboard!', 'Please do not copy during your test.')
    }
    (async () => {
        const current_active_app_title = (await activeWin()).title;
        if (current_active_app_title !== previous_active_app_title) {
            previous_active_app_title = current_active_app_title
            showNotification('Active window changed to ' + current_active_app_title + '!', 'Please do not switch to other apps during your test.')
        }
    })();
}, 2000);

app.setAppUserModelId("com.electron.vega")
// app.setPath("userData", __dirname + "/saved_recordings")

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        },
        icon: './vega.png'
    })

    // win.loadFile('index.html')
    win.webContents.openDevTools()
    win.loadURL(url.format({
        pathname: path.join(__dirname, '../renderer/index.html'),
        protocol: 'file:',
        slashes: true
    }))
}

function showNotification(title, body) {
    console.log("Show notification")
    const notification = {
        title: title,
        body: body
    }
    new Notification(notification).show()
}

app.whenReady().then(createWindow).then(showNotification)

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