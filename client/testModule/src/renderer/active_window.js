const activeWin = require('active-win');

let previous_active_app_title =  (async () => {
    active_app_title = (await activeWin()).title;
})();

const active_window_interval = setInterval(function() {
    const current_clipboard = clipboardy.readSync()
    (async () => {
        const current_active_app_title = (await activeWin()).title;
        if (current_active_app_title !== previous_active_app_title) {
            previous_active_app_title = current_active_app_title
            showNotification('Active window changed to ' + current_active_app_title, 'Please do not switch to other apps during your test.', 'electron-activewindow')
        }
    })();
}, 2000);