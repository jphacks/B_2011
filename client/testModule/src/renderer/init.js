const { ipcRenderer } = require('electron')

ipcRenderer.send('dual_display_detect', { description: 'start dual display detect' });

const add_warning = (warning_message) => {
  let warning = document.getElementById('warning')
  let new_warning = document.createElement('li')
  new_warning.innerText = warning_message
  warning.appendChild(new_warning)
  new_warning.scrollIntoView()
}

ipcRenderer.on('proctor-message', (event, message) => {
  let proctor = document.getElementById('proctor-message')
  let new_message = document.createElement('li')
  new_message.innerText = message
  proctor.appendChild(new_message)
  new_message.scrollIntoView()
})
