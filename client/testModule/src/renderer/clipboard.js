const clipboardy = require('clipboardy')

let previous_clipboard = clipboardy.readSync();
const clipboard_interval = setInterval(function() {
    const current_clipboard = clipboardy.readSync()
	if (current_clipboard !== previous_clipboard) {
        previous_clipboard = current_clipboard
        const myNotification = new Notification('Copied to Clipboard!', {
            body: 'Please do not copy during your test.'
        })
        ipcRenderer.send('clipboard', { description: 'User copied something.' });
    }
}, 2000);