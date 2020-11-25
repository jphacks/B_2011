const activeWin = require('active-win')
const helper = require('../helper')

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
            helper.send_json("active_window", "Changed to " + current_active_app_title)
        }
    })();
}, 2000);