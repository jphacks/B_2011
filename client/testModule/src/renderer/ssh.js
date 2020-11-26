const sudo = require('sudo-prompt');
const ipc = require('node-ipc');
const { ipcRenderer } = require('electron');

const options = {
    name: 'SATORI',
    icns: '../main/satori.png',
};
ipc.config.id = 'sshserver';
ipc.config.retry = 1500;

ipc.serve(function() {
    ipc.server.on('message', function(data) {
        ipcRenderer.send(data.module, { description: data.body });
    });
});

ipc.server.start();

// sudo-prompt does not provide stdout stream, so use ipc
sudo.exec('node ./src/renderer/process/packet.js', options, (err) => {
    if (err)  throw err;
});