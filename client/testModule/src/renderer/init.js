const { ipcRenderer } = require('electron')

ipcRenderer.send('dual_display_detect', { description: 'start dual display detect' });