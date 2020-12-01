const clipboardy = require('clipboardy')
let clipboard_counter = 0

let previous_clipboard = clipboardy.readSync();
const clipboard_interval = setInterval(function() {
    const current_clipboard = clipboardy.readSync()
	if (current_clipboard !== previous_clipboard) {
        previous_clipboard = current_clipboard
        const myNotification = new Notification('Copied to Clipboard!', {
            body: 'Please do not copy during your test.'
        })
        ipcRenderer.send('clipboard', {
            alert: 2,
            description: 'User copied something.'
        });
    } else {
        clipboard_counter += 1
        if (clipboard_counter == 4) {
            ipcRenderer.send('clipboard', {
                alert: 0,
                description: 'normal'
            });
            clipboard_counter = 0
        }
    }
}, 2000);