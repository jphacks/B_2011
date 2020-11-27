const { ipcRenderer, screen } = require('electron');

const multiscreen_interval = setInterval(function() {
    let displays = screen.getAllDisplays()
    let externalDisplay = displays.find((display) => {
        return display.bounds.x !== 0 || display.bounds.y !== 0
    })
    if (externalDisplay) {
        const myNotification = new Notification('Second screen detected.', {
            body: 'You cannot use second screen.'
        });
        console.log('second screen detected!');
        ipcRenderer.send('second_screen', { description: 'Second screen detected' });
    }
}, 2000);