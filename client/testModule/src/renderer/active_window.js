const activeWin = require('active-win')
const { ipcRenderer } = require('electron')
let active_window_counter = 0;

let previous_active_app_title =  (async () => {
    active_app_title = (await activeWin()).title;
})();

const active_window_interval = setInterval(function() {
    (async () => {
        const current_active_app_title = (await activeWin()).title;
        if (current_active_app_title !== previous_active_app_title) {
            previous_active_app_title = current_active_app_title
            const myNotification = new Notification('Active window changed to ' + current_active_app_title, {
                body: 'Please do not switch to other apps during your test.'
            })
            ipcRenderer.send('active_window', {
                alert: 2,
                description: 'Changed to ' + current_active_app_title 
            });
        } else {
            active_window_counter += 1
            if (active_window_counter == 4) {
                ipcRenderer.send('active_window', {
                    alert: 0,
                    description: 'normal'
                });
                active_window_counter = 0
            }
        }
    })();
}, 2000);