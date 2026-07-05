const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("neon", {
  version: "0.1.0",
  mode: "visual-prototype"
});
