const electron = require('electron')
const { app, BrowserWindow } = require('electron')

const multiscreen_interval = setInterval(function() {
    let displays = screen.getAllDisplays()
    let externalDisplay = displays.find((display) => {
        return display.bounds.x !== 0 || display.bounds.y !== 0
    })
    if (externalDisplay) {
        const myNotification = new Notification('Second screen detected.', {
            body: 'You cannot use second screen.'
        })
        ipcRenderer.send('Second screen', { description: 'Second screen detected' });
    }
}, 2000);