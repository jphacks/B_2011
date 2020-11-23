document.querySelector('#submit').addEventListener('click', () => {
    const exam_id = document.getElementById("exam_id").value;
    const user_id = document.getElementById("user_id").value;

    const { ipcRenderer } = require('electron')
    ipcRenderer.send('asynchronous-message', {exam_id: exam_id, user_id: user_id} )
    document.location.href = "take_photo.html"
})