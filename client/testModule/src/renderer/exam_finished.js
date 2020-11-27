document.getElementById('quit_app').onclick = () => {
  const { ipcRenderer } = require('electron')
  ipcRenderer.send('exam_finished')
}