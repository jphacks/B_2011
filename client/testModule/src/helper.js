// helper.js
// Helper functions for SATORI Desktop App.

const http = require('http')
const { ipcRenderer } = require('electron')

function send_json(module_name, description, content) {
    
    let exam_id = '911f6e61-e061-4be9-9f25-246e1fb16207';
    let user_id = '911f6e61-e061-4be9-9f25-246e1fb16207'

    ipcRenderer.send('get_user_data');
    ipcRenderer.on('get_user_data', (event, data) => {
        exam_id = data.exam_id
        user_id = data.user_id
    });

    const data = JSON.stringify([{
        "examinee_id": user_id,
        "exam_id": exam_id,
        "module_name": module_name,
        "alert": "True",
        "description": description,
        "content": content,
    }])

    const options = {
        hostname: 'demo.ben.hongo.wide.ad.jp',
        port: 8000,
        path: '/api/message/list',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': data.length
        }
    }

    const req = http.request(options, res => {
        console.log(`statusCode: ${res.statusCode}`)
      
        res.on('data', d => {
            process.stdout.write(d)
        })
    })

    req.on('error', error => {
        console.error(error)
    })

    req.write(data)
    req.end()
}

module.exports = { send_json }
