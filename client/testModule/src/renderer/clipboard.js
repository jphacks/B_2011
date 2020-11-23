const clipboardy = require('clipboardy');

let previous_clipboard = clipboardy.readSync();
const clipboard_interval = setInterval(function() {
    const current_clipboard = clipboardy.readSync()
	if (current_clipboard !== previous_clipboard) {
        previous_clipboard = current_clipboard
        showNotification('Copied to Clipboard!', 'Please do not copy during your test.', 'electron-clipboard')
    }
}, 2000);

function showNotification(title, body, module) {
    console.log("[notification] " + title + ' ' +  body)
    const notification = {
        title: title,
        body: body,
        icon: nativeImage.createFromPath(path.join(__dirname, 'satori.png'))
    }
    new Notification(notification).show()
}