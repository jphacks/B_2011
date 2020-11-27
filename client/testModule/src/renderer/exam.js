// Open Exam link in external browser
document.getElementById('exam_link').innerText = "http://google.com"
document.getElementById('exam_link').onclick = () => {
    const { shell } = require('electron')
    shell.openExternal('https://google.com')
}

document.getElementById('exam_finish').onclick = () => {
    document.location.href = "exam_finished.html"
}