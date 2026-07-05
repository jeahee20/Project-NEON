const { app, BrowserWindow, Menu } = require("electron");
const path = require("path");

function createWindow() {
  Menu.setApplicationMenu(null);

  const win = new BrowserWindow({
    width: 1280,
    height: 820,
    minWidth: 1080,
    minHeight: 700,
    backgroundColor: "#050509",
    title: "Project NEON",
    autoHideMenuBar: true,
    show: false,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  win.webContents.on("did-finish-load", () => {
    win.webContents.setZoomFactor(1);
  });

  win.once("ready-to-show", () => {
    win.show();
  });

  win.loadFile("index.html");
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
