const AsyncLock = require('async-lock');
const Cap = require('cap').Cap;
const decoders = require('cap').decoders;
const PROTOCOL = decoders.PROTOCOL;
const fetch = require('node-fetch');
const si = require('systeminformation');
const ipc = require('node-ipc');

ipc.config.id = 'sshclient';
ipc.config.retry = 1500;

const sleep = async (ms) => {
    return await new Promise(r => {
        setTimeout(r, ms);
    });
};

const detectDevices = async () => {
    const deviceList = Cap.deviceList();
    for (const device of deviceList) {
        for (const addr of device.addresses) {
            if (addr.netmask === undefined) {
                continue;
            }
            const c = new Cap();
            const filter = "tcp and src port 8000";
            const bufSize = 10 * 1024 * 1024;
            const buffer = Buffer.alloc(65535);
            const linkType = c.open(device.name, filter, bufSize, buffer);
            c.setMinBytes && c.setMinBytes(0);
            let ok = false;
            c.on('packet', () => {
                if (linkType === 'ETHERNET') {
                    const eth = decoders.Ethernet(buffer);
                    const internet = eth.info.type === PROTOCOL.ETHERNET.IPV4 ? decoders.IPV4(buffer, eth.offset) :
                        eth.info.type === PROTOCOL.ETHERNET.IPV6 ? decoders.IPV6(buffer, eth.offset) :
                            null;
                    if (internet === null) {
                        return;
                    }
                    const saddr = internet.info.srcaddr;
                    const daddr = internet.info.dstaddr;
                    if (daddr !== addr.addr) {
                        return;
                    }
                    const trans = internet.info.protocol === PROTOCOL.IP.TCP ? decoders.TCP(buffer, internet.offset) :
                        internet.info.protocol === PROTOCOL.IP.UDP ? decoders.UDP(buffer, internet.offset) :
                            null;
                    if (trans === null) {
                        return;
                    }
                    const sport = trans.info.srcport;
                    if (sport !== 8000) return;
                    ok = true;
                }
            });
            
            while (true) {
                const response = await fetch('http://203.178.135.71:8000/ping');
                if (response.status === 200) {
                    break;
                }
            }

            await sleep(1000);
            if (ok) {
                return {
                    device,
                    ipAddr: addr.addr,
                };
            }
        }
    }
    return null;
};

const testSSH = async () => {
    const { device, ipAddr } = await detectDevices();
    if (device === null) {
        console.error('I think that there is no devices that connect to the Internet...');
    }

    ipc.connectTo('sshserver', function() {
        ipc.of.sshserver.on('connect', function() {
            const c = new Cap();
            const filter = "";
            const bufSize = 10 * 1024 * 1024;
            const buffer = Buffer.alloc(65535);
            const linkType = c.open(device.name, filter, bufSize, buffer);
            c.setMinBytes && c.setMinBytes(0);

            const lock = new AsyncLock({ timeout: 1000 });
            let portTraffics = {};
            c.on('packet', (nbytes, _) => {
                if (linkType === 'ETHERNET') {
                    const eth = decoders.Ethernet(buffer);
                    const internet = eth.info.type === PROTOCOL.ETHERNET.IPV4 ? decoders.IPV4(buffer, eth.offset) :
                        eth.info.type === PROTOCOL.ETHERNET.IPV6 ? decoders.IPV6(buffer, eth.offset) :
                            null;
                    if (internet === null) {
                        return;
                    }
                    const saddr = internet.info.srcaddr;
                    const daddr = internet.info.dstaddr;
                    if (saddr !== ipAddr && daddr !== ipAddr) {
                        return;
                    }
                    const trans = internet.info.protocol === PROTOCOL.IP.TCP ? decoders.TCP(buffer, internet.offset) :
                        internet.info.protocol === PROTOCOL.IP.UDP ? decoders.UDP(buffer, internet.offset) :
                            null;
                    if (trans === null) {
                        return;
                    }
                    const sport = trans.info.srcport;
                    const dport = trans.info.dstport;
                    lock.acquire("portTraffics", () => {
                        if (saddr === ipAddr) {
                            portTraffics[sport] = portTraffics[sport] ? portTraffics[sport] + nbytes : nbytes;
                        }
                        else {
                            portTraffics[dport] = portTraffics[dport] ? portTraffics[dport] + nbytes : nbytes;
                        }
                    });
                }
            });
        
            const checkProcessName = (process) => {
                // Chrome remote desktop@Windows
                if (/.*(remote|remoting).*/.test(process.name)) {
                    return true;
                }
                // ssh@Ubuntu
                else if (/.*sshd: .*/.test(process.command)) {
                    return true;
                }
                return false;
            };

            setInterval(async () => {
                // process name filtering
                const processList = (await si.processes()).list;
                const alertProcessList = processList.filter((process) => checkProcessName(process));
                if (alertProcessList.length === 0) {
                    ipc.of.sshserver.emit('message', {
                        title: 'ok',
                        alert: 0,
                        description: 'no problem',
                        module: 'ssh_process_name',
                    });
                } else {
                    // alert(level=warning?)
                    const processNameList = alertProcessList.map(process => `${process.pid}: ${process.name}`);
                    ipc.of.sshserver.emit('message', {
                        title: 'suspicious process detected',
                        alert: 1,
                        description: JSON.stringify(processNameList),
                        module: 'ssh_process_name',
                    });
                }
                
                // network traffic filtering
                const port2pid = {};
                (await si.networkConnections()).forEach((conn) => {
                    if (conn.pid === '0' || conn.pid === undefined) {
                        return;
                    }
                    else if (conn.localport === '') {
                        return;
                    }
                    port2pid[conn.localport] = conn.pid;
                });
                const pid2process = {};
                processList.forEach(process => {
                    pid2process[process.pid] = process;
                });

                let portList = null;
                await lock.acquire('portTraffics', () => {
                    portList = Object.entries(portTraffics);
                    portTraffics = {};
                });
                const alertPortList = portList.filter(val => {
                    const [_, nbytes] = val;
                    return nbytes > 1 * 5 * 1024 * 1024; // 1MB/s
                });
                if (alertPortList.length === 0) {
                    ipc.of.sshserver.emit('message', {
                        title: 'ok',
                        alert: 0,
                        description: 'no problem',
                        module: 'ssh_network_traffic',
                    });
                } else {
                    // alert(level=warning?)
                    const portDetails = alertPortList.map(val => {
                        let [port, nbytes] = val;
                        port = port.toString();
                        nbytes /= 5.0 * 1024 * 1024;
                        let pid = port2pid[port] || -1;
                        let process = pid2process[pid.toString()] || null;
                        return {
                            port,
                            traffic: `${nbytes}MB/s`,
                            process: process.name,
                        };
                    });
                    ipc.of.sshserver.emit('message', {
                        title: 'over-traffic process detected',
                        alert: 1,
                        description: JSON.stringify(portDetails),
                        module: 'ssh_network_traffic',
                    });
                }
            }, 5000);
        });
    });
};

testSSH();
