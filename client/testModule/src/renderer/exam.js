let exam_id = ''
let exam_url = ''
let exam_name = ''
let exam_description = ''
let exam_date = ''
let exam_start_at = ''
let exam_end_at = ''

// IPC: Request User Info (exam_id and user_id)
ipcRenderer.send('exam', 'get_user_info');
ipcRenderer.on('exam', (event, data) => {
    document.getElementById('exam_id').innerText = data.exam_id
    document.getElementById('user_id').innerText = data.user_id
    exam_id = data.exam_id

    const exam_info_url = "http://203.178.135.71:8000/api/exam/?exam_id=" + exam_id
    fetch(exam_info_url)
        .then(response => response.json())
        .then(data => {
            const obj = JSON.parse(data)
            exam_url = obj.exam_data.exam_url
            exam_name = obj.exam_data.exam_name
            exam_description = obj.exam_data.description
            exam_date = obj.exam_data.exam_date
            exam_start_at = obj.exam_data.start_at
            exam_end_at = obj.exam_data.end_at


            // Open Exam link in external browser
            document.getElementById('exam_link').innerText = exam_url
            document.getElementById('exam_name').innerText = exam_name
            document.getElementById('exam_description').innerText = exam_description
            document.getElementById('exam_date').innerText = exam_date
            document.getElementById('exam_start_at').innerText = exam_start_at
            document.getElementById('exam_end_at').innerText = exam_end_at
            document.getElementById('exam_link').onclick = () => {
                const { shell } = require('electron')
                shell.openExternal(exam_url)
            }

        })
});
document.getElementById('exam_finish').onclick = () => {
    document.location.href = "exam_finished.html"
}