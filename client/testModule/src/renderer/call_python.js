const PY_DIST_FOLDER = 'python_dist'
const PY_FOLDER = 'python_code'
const PY_MODULE = 'calc_similarity' // without .py suffix

const dist_folder_exists = () => {
    const fullPath = path.join(__dirname, '..', '..', PY_DIST_FOLDER)
    return require('fs').existsSync(fullPath)
}

const getScriptPath = () => {
    if (!dist_folder_exists()) {
      return path.join(__dirname, '..', '..', PY_FOLDER, PY_MODULE + '.py')
    }
    return path.join(__dirname, '..', '..', PY_DIST_FOLDER, PY_MODULE)
}

const script = getScriptPath()

if (!dist_folder_exists()) {
    // Execute Python using Python-shell when dist folder does not exist
    const ps = require('python-shell')
    let pyshell = new ps.PythonShell(script)
    console.log('Python script started')
    pyshell.on('message', (message) => {
      console.log(message);
    });
} else {
    // Execute python dist file when its available
    const { spawn } = require('child_process');
    const ls = spawn(script);
    ls.stdout.on('data', (data) => {
      myConsole.log(`${data}`);
      document.getElementById('counter').innerText = data;
    });
}