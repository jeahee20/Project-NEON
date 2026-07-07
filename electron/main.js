const { app, BrowserWindow, Menu, ipcMain } = require("electron");
const { spawn } = require("child_process");
const http = require("http");
const path = require("path");

const BACKEND_HOST = "127.0.0.1";
const BACKEND_PORT = 5050;
const BACKEND_HEALTH_PATH = "/health";
const PROJECT_ROOT = path.resolve(__dirname, "..");
const BACKEND_SCRIPT = path.join(PROJECT_ROOT, "backend", "server.py");

let mainWindow = null;
let backendProcess = null;
let backendStartedByElectron = false;
let backendStatus = "connecting";
let backendReason = "boot";
let appIsQuitting = false;

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

  mainWindow = win;

  win.webContents.on("did-finish-load", () => {
    win.webContents.setZoomFactor(1);
    sendBackendStatusToRenderer();
  });

  win.once("ready-to-show", () => {
    win.show();
  });

  win.on("closed", () => {
    if (mainWindow === win) mainWindow = null;
  });

  win.loadFile("index.html");
}

function setBackendStatus(status, reason = "") {
  backendStatus = status;
  backendReason = reason;
  sendBackendStatusToRenderer();
}

function sendBackendStatusToRenderer() {
  if (!mainWindow || mainWindow.isDestroyed()) return;
  mainWindow.webContents.send("backend:status", getBackendStatusPayload());
}

function getBackendStatusPayload() {
  return {
    status: backendStatus,
    reason: backendReason,
    url: `http://${BACKEND_HOST}:${BACKEND_PORT}`,
    startedByElectron: backendStartedByElectron
  };
}

function checkBackendHealth(timeoutMs = 900) {
  return new Promise((resolve) => {
    const request = http.request(
      {
        hostname: BACKEND_HOST,
        port: BACKEND_PORT,
        path: BACKEND_HEALTH_PATH,
        method: "GET",
        timeout: timeoutMs
      },
      (response) => {
        let body = "";
        response.setEncoding("utf8");
        response.on("data", (chunk) => {
          body += chunk;
        });
        response.on("end", () => {
          if (response.statusCode !== 200) {
            resolve(false);
            return;
          }
          try {
            const data = JSON.parse(body);
            resolve(data.status === "online" || data.brain_loaded === true);
          } catch (error) {
            resolve(false);
          }
        });
      }
    );

    request.on("timeout", () => {
      request.destroy();
      resolve(false);
    });

    request.on("error", () => {
      resolve(false);
    });

    request.end();
  });
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForBackendOnline(timeoutMs = 15000) {
  const startedAt = Date.now();
  while (Date.now() - startedAt < timeoutMs) {
    if (await checkBackendHealth()) return true;
    await delay(500);
  }
  return false;
}

async function ensureBackend() {
  setBackendStatus("connecting", "checking existing backend");

  if (await checkBackendHealth()) {
    backendStartedByElectron = false;
    setBackendStatus("online", "existing backend");
    return;
  }

  try {
    backendProcess = spawn("py", [BACKEND_SCRIPT], {
      cwd: PROJECT_ROOT,
      windowsHide: true,
      stdio: ["ignore", "pipe", "pipe"]
    });
    backendStartedByElectron = true;
    setBackendStatus("connecting", "starting python backend");
  } catch (error) {
    backendStartedByElectron = false;
    backendProcess = null;
    setBackendStatus("failed", `python spawn failed: ${error.message}`);
    return;
  }

  backendProcess.stdout.on("data", (data) => {
    console.log(`[NEON BACKEND] ${String(data).trim()}`);
  });

  backendProcess.stderr.on("data", (data) => {
    console.warn(`[NEON BACKEND] ${String(data).trim()}`);
  });

  backendProcess.on("error", (error) => {
    setBackendStatus("failed", `python error: ${error.message}`);
  });

  backendProcess.on("exit", (code) => {
    const wasOwned = backendStartedByElectron;
    backendProcess = null;
    backendStartedByElectron = false;
    if (!appIsQuitting && wasOwned) {
      setBackendStatus(code === 0 ? "offline" : "failed", `backend exited: ${code}`);
    }
  });

  if (await waitForBackendOnline()) {
    setBackendStatus("online", "python backend ready");
  } else {
    setBackendStatus("failed", "backend health timeout");
  }
}

function stopOwnedBackend() {
  if (!backendProcess || !backendStartedByElectron) return;
  try {
    backendProcess.kill();
  } catch (error) {
    console.warn(`[NEON BACKEND] stop failed: ${error.message}`);
  }
}

ipcMain.handle("backend:get-status", () => getBackendStatusPayload());

app.whenReady().then(() => {
  setBackendStatus("connecting", "boot");
  createWindow();
  ensureBackend();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("before-quit", () => {
  appIsQuitting = true;
  stopOwnedBackend();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
