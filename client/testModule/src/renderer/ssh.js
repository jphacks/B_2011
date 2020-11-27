const sudo = require('sudo-prompt');
const ipc = require('node-ipc');

const options = {
    name: 'SATORI',
    icns: '../main/satori.png',
};
ipc.config.id = 'sshserver';
ipc.config.retry = 1500;

ipc.serve(function() {
    ipc.server.on('message', function(data) {
        // new Notification(data.description);
        ipcRenderer.send(data.module, data);
    });
});

ipc.server.start();

// sudo-prompt does not provide stdout stream, so use ipc
// If you want to debug this process, please comment out exec command and use another terminal.
sudo.exec('node ' + require('path').resolve('./src/renderer/process/packet.js'), options, (err) => {
    if (err)  throw err;
});
