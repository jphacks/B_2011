// helper.js
// Helper functions for SATORI Desktop App.

const http = require('http')

function send_json(user_id, exam_id, module_name, description, content) {
    
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
