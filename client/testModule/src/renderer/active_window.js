const activeWin = require('active-win')

let previous_active_app_title = (async() => {
    active_app_title = (await activeWin()).title;
})();

const active_window_interval = setInterval(function() {
    (async() => {
        const current_active_app_title = (await activeWin()).title;
        if (current_active_app_title !== previous_active_app_title) {
            previous_active_app_title = current_active_app_title
            const myNotification = new Notification('Active window changed to ' + current_active_app_title, {
                body: 'Please do not switch to other apps during your test.'
            })
            ipcRenderer.send('active_window', { description: 'Changed to ' + current_active_app_title });
        }
    })();
}, 2000);