const clipboardy = require('clipboardy')
const helper = require('../helper')

let previous_clipboard = clipboardy.readSync();
const clipboard_interval = setInterval(function() {
    const current_clipboard = clipboardy.readSync()
	if (current_clipboard !== previous_clipboard) {
        previous_clipboard = current_clipboard
        const myNotification = new Notification('Copied to Clipboard!', {
            body: 'Please do not copy during your test.'
        })
        helper.send_json("active_window", "Changed to " + current_active_app_title)
    }
}, 2000);