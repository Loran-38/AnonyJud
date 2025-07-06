const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let backendProcess;

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });
  win.loadURL('http://localhost:3000');
}

app.whenReady().then(() => {
  // Lancer le backend Python
  backendProcess = spawn('python', [path.join(__dirname, '../../anonyjud-backend/start_backend.py')], {
    stdio: 'inherit',
    shell: true,
  });
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
  if (backendProcess) backendProcess.kill();
}); 