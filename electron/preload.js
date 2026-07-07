const { contextBridge, ipcRenderer } = require("electron");
const fs = require("fs");
const path = require("path");

function loadJsonDialogueFile(fileName) {
  const filePath = path.join(__dirname, "assets", "dialogues", fileName);
  const raw = fs.readFileSync(filePath, "utf8");
  return JSON.parse(raw);
}

function loadLegacyPhrases() {
  return loadJsonDialogueFile("legacy_phrases.json");
}

function loadHomeGreetings() {
  return loadJsonDialogueFile("home_greetings.json");
}

contextBridge.exposeInMainWorld("neon", {
  version: "0.1.0",
  mode: "visual-prototype",
  loadLegacyPhrases,
  loadHomeGreetings,
  getBackendStatus: () => ipcRenderer.invoke("backend:get-status"),
  onBackendStatus: (callback) => {
    if (typeof callback !== "function") return () => {};
    const listener = (_event, status) => callback(status);
    ipcRenderer.on("backend:status", listener);
    return () => ipcRenderer.removeListener("backend:status", listener);
  }
});
