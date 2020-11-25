
// IPC with main-process
const { ipcRenderer } = require('electron')
// IPC: Request User Info (exam_id and user_id)
ipcRenderer.send('exam_prep', 'get_user_info');
ipcRenderer.on('exam_prep', (event, data) => {
    document.getElementById('exam_id').innerText = data.exam_id
    document.getElementById('user_id').innerText = data.user_id
});

// Open Exam link in external browser
document.getElementById('exam_link').innerText = "http://google.com"
document.getElementById('exam_link').onclick = () => {
    const { shell } = require('electron')
    shell.openExternal('https://google.com')
}

document.getElementById('exam_start').onclick = () => {
    document.location.href = "exam.html"
}