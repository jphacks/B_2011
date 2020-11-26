const sudo = require('sudo-prompt');
const options = {
    name: 'SATORI',
    icns: '../main/satori.png',
};

const ssh_main = async () => {
    // sudo-prompt does not provide stdout stream, so called process must create output file, and this file will read it.
    sudo.exec('node ./src/renderer/process/packet.js', options, (err, _, _) => {
        if (err)  throw err;
    });

    const readStream = fs.createReadStream('./src/renderer/process/out.txt', 'utf8');
    readStream.on('data', (chunk) => {
        new Notification(chunk);
    });
};

ssh_main();
