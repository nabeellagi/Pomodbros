const { app, BrowserWindow } = require('electron');
const path = require('path');

const isDev = !app.isPackaged;
// const URL = "http://localhost:5173/";
const URL = "http://localhost:5173/testings/font";

const DIST = path.join(__dirname, '..', 'app', 'dist', 'index.html') // Vite build output

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 800,
        autoHideMenuBar: true,
        resizable: false,
        maximizable: false,
        webPreferences: {
            devTools: isDev,
            contextIsolation: true,
            nodeIntegration: false
        }
    });


    win.webContents.on('dom-ready', () => {
        win.webContents.setZoomFactor(1.1);
    })

    if(isDev){
        win.loadURL(URL);
    }else{
        win.loadFile(DIST);
    }
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
    if (process.platform != 'darwin') app.quit();
})