document.querySelector('#submit').addEventListener('click', () => {
    let exam_id = document.getElementById("exam_id").value;
    let user_id = document.getElementById("user_id").value;

    // Check if exam_id and user_id is an UUID4
    exam_id = exam_id.match('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    user_id = user_id.match('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')

    // If exam_id or user_id is not UUID4, alert user and stop function
    if (exam_id === null || user_id === null) {
        alert('Exam ID or User ID is not correct')
        return false
    }

    // Send the exam_id and user_id to main-process
    const { ipcRenderer } = require('electron')
    ipcRenderer.send('asynchronous-message', {
        exam_id: exam_id[0],
        user_id: user_id[0]
    })

    // Proceed to next page
    document.location.href = "take_photo.html"
})