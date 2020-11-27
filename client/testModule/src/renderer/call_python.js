const PY_DIST_FOLDER = 'python_dist'
const PY_FOLDER = 'python_code'
const PY_CALC_DIST = 'calc_similarity' // without .py suffix
const PY_VOICE = 'voice'
const PY_VOICE_DETECT = 'voice_anomaly_detection' // without .py suffix

const dist_folder_exists = () => {
    const fullPath = path.join(__dirname, '..', '..', PY_DIST_FOLDER)
    return require('fs').existsSync(fullPath)
}

const getScriptPath = () => {
    if (!dist_folder_exists()) {
      const path_calc_dist = path.join(__dirname, '..', '..', PY_FOLDER, PY_CALC_DIST + '.py');
      const path_voice_detect = path.join(__dirname, '..', '..', PY_FOLDER, PY_VOICE, PY_VOICE_DETECT + '.py');
      const array = [path_calc_dist, path_voice_detect];
      return array
    }
    const path_calc_dist = path.join(__dirname, '..', '..', PY_FOLDER, PY_CALC_DIST);
    const path_voice_detect = path.join(__dirname, '..', '..', PY_FOLDER, PY_VOICE, PY_VOICE_DETECT);
    const array = [path_calc_dist, path_voice_detect];
    return array
}

const scripts = getScriptPath()

if (!dist_folder_exists()) {
    // Execute Python using Python-shell when dist folder does not exist
    const ps = require('python-shell')
    for(let i = 0; i < 2; i++){
      let pyshell = new ps.PythonShell(scripts[i])
      console.log('Python script started')
      const { ipcRenderer } = require('electron')
      pyshell.on('message', (message) => {
        const data = JSON.parse(message)
        if (data.alert !== 0) {
          const myNotification = new Notification(data.description, {
            body: ''
          })
        }
        ipcRenderer.send(data.module, {
          alert: data.alert,
          description: data.description
        })
      });
    }
} else {
    // Execute python dist file when its available
    const { spawn } = require('child_process');
    for(let i = 0; i < scripts.length; i++){
      const ls = spawn(scripts[i]);
      ls[i].stdout.on('data', (data) => {
        myConsole.log(`${data}`);
        document.getElementById('counter').innerText = data;
      });
    }
}