const captureVideoFrame = require('capture-video-frame')
const dataUriToBuffer = require('data-uri-to-buffer')
const fs = require('fs')
const path = require('path')

function saveCanvas () {
    const frame = captureVideoFrame.captureVideoFrame("video", "png");
    const decoded = dataUriToBuffer(frame.dataUri)
    fs.writeFile(path.join(__dirname, '../../../img/sample.png'), decoded, (err) => {
      if (err) {
        console.log('ファイルの保存に失敗しました')
        console.log(err)
      } else {
        // console.log('ファイルを保存しました')
      }
    })

}

setInterval(() => {
    saveCanvas()
}, 5000)