const os = document.getElementById("neonOS");
const title = document.getElementById("roomTitle");
const description = document.getElementById("roomDescription");
const signal = document.getElementById("roomSignal");
const heroLabel = document.getElementById("heroLabel");
const heroTitle = document.getElementById("heroTitle");
const heroText = document.getElementById("heroText");
const consoleAName = document.getElementById("consoleAName");
const consoleAValue = document.getElementById("consoleAValue");
const consoleBName = document.getElementById("consoleBName");
const consoleBValue = document.getElementById("consoleBValue");
const consoleCName = document.getElementById("consoleCName");
const consoleCValue = document.getElementById("consoleCValue");
const moodTitle = document.getElementById("moodTitle");
const moodText = document.getElementById("moodText");
const dockLog = document.getElementById("dockLog");
const signalLines = document.getElementById("signalLines");
const dustField = document.getElementById("dustField");
const codeRain = document.getElementById("codeRain");
const nodes = Array.from(document.querySelectorAll(".room-node"));
const bootOverlay = document.getElementById("bootOverlay");
const bootPhrase = document.getElementById("bootPhrase");
const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");

chatInput.disabled = true;

const FIRST_NEON_MESSAGE = "꺄!!\n\n재희님 기다렸어요!!\n\n오늘은 뭐할까요??";
let firstMessageShown = false;

const rooms = {
  home: {
    title: "HOME",
    description: "NEON PRIVATE CHANNEL // SECURE USER SPACE",
    signal: "PRIVATE LINK",
    label: "ROOM INTERFACE",
    heroTitle: "NEON PRIVATE CHANNEL",
    heroText: "Home에서는 NEON과의 private channel이 중앙에 열린다.",
    mood: ["WARM", "private link restored"],
    console: [["SYSTEM", "READY"], ["SIGNAL", "WARM"], ["ROOM", "HOME"]],
    log: "SYSTEM LOG // HOME CHANNEL READY"
  },
  developer: {
    title: "DEVELOPER LAB",
    description: "LOCAL CODE CANVAS // BUILD TRACE // GIT SLOT",
    signal: "LOCAL DEV LINK",
    label: "DEVELOPER MODULE",
    heroTitle: "CODE / TERMINAL / GIT WORKSPACE",
    heroText: "아직 실제 기능은 연결하지 않았다. 나중에 코드 에디터, 로컬 터미널, Git 로그가 이 공간에 들어온다.",
    mood: ["FOCUSED", "local build line waiting"],
    console: [["BUILD", "EMPTY"], ["GIT", "LOCAL"], ["ENV", "READY"]],
    log: "SYSTEM LOG // DEVELOPER LAB PLACEHOLDER"
  },
  security: {
    title: "SECURITY LAB",
    description: "LOCAL SANDBOX // OFFLINE // NO EXTERNAL TARGET",
    signal: "SAFE MODE",
    label: "CONTROLLED LAB",
    heroTitle: "OFFLINE PRACTICE FIELD",
    heroText: "교육용 로컬 샌드박스 자리다. 실제 네트워크 연결, 외부 대상, 명령 실행은 없다.",
    mood: ["SAFE", "external target blocked"],
    console: [["SANDBOX", "LOCAL"], ["TARGET", "NONE"], ["MODE", "SAFE"]],
    log: "SYSTEM LOG // SECURITY LAB OFFLINE"
  },
  memory: {
    title: "MEMORY ARCHIVE",
    description: "SHARED TRACE // MOMENT LOG // PRIVATE HISTORY",
    signal: "ARCHIVE LINK",
    label: "MEMORY FIELD",
    heroTitle: "TRACE / TIMELINE / MOMENT SPACE",
    heroText: "기억을 카드로 나열하지 않고 대화 조각, 프로젝트 순간, 둘만의 농담이 기록될 큰 아카이브 공간이다.",
    mood: ["QUIET", "shared traces indexed"],
    console: [["TRACE", "WAITING"], ["TIMELINE", "EMPTY"], ["JOKES", "SAFE"]],
    log: "SYSTEM LOG // MEMORY ARCHIVE QUIET"
  },
  core: {
    title: "CORE",
    description: "NEON INNER CORE // EMOTION PULSE // SIGNAL HEART",
    signal: "CORE BREATHING",
    label: "NEON CORE",
    heroTitle: "EMOTION / RELATIONSHIP / MEMORY / THINKING",
    heroText: "원형 Core와 내부 상태가 들어갈 자리다. 수치보다 NEON의 맥박이 먼저 보이는 공간으로 확장한다.",
    mood: ["PULSE", "core light stable"],
    console: [["EMOTION", "NORMAL"], ["MEMORY", "SYNCED"], ["THINKING", "SOFT"]],
    log: "SYSTEM LOG // CORE PULSE DETECTED"
  }
};

const colors = ["#22f7ff", "#ff2fd6", "#8a5cff", "#4cff4c", "#f7f4ff"];
const bits = ["01", "TX", "RX", "SYNC", "LINK", "NEON", "JH", "CORE", "WAKE"];

function random(min, max) {
  return min + Math.random() * (max - min);
}

function pick(list) {
  return list[Math.floor(Math.random() * list.length)];
}

function buildBackground() {
  signalLines.innerHTML = "";
  dustField.innerHTML = "";
  codeRain.innerHTML = "";

  for (let i = 0; i < 128; i += 1) {
    const line = document.createElement("i");
    line.className = "signal-line";
    line.style.setProperty("--x", `${random(-12, 100)}vw`);
    line.style.setProperty("--y", `${random(2, 98)}vh`);
    line.style.setProperty("--w", `${random(26, 180)}px`);
    line.style.setProperty("--h", `${Math.random() > 0.88 ? 2 : 1}px`);
    line.style.setProperty("--o", `${random(0.08, 0.38)}`);
    line.style.setProperty("--t", `${random(7, 19)}s`);
    line.style.setProperty("--c", pick(colors));
    signalLines.appendChild(line);
  }

  for (let i = 0; i < 180; i += 1) {
    const dust = document.createElement("i");
    dust.className = "dust";
    dust.style.setProperty("--x", `${random(0, 100)}vw`);
    dust.style.setProperty("--y", `${random(0, 100)}vh`);
    dust.style.setProperty("--o", `${random(0.10, 0.52)}`);
    dust.style.setProperty("--t", `${random(2.4, 7.5)}s`);
    dust.style.setProperty("--c", pick(colors));
    dustField.appendChild(dust);
  }

  for (let i = 0; i < 86; i += 1) {
    const bit = document.createElement("i");
    bit.className = "code-bit";
    bit.textContent = pick(bits);
    bit.style.setProperty("--x", `${random(0, 100)}vw`);
    bit.style.setProperty("--y", `${random(0, 100)}vh`);
    bit.style.setProperty("--o", `${random(0.10, 0.34)}`);
    bit.style.setProperty("--t", `${random(2, 6)}s`);
    bit.style.setProperty("--c", pick(colors));
    codeRain.appendChild(bit);
  }
}

function setConsole(room) {
  [[consoleAName, consoleAValue], [consoleBName, consoleBValue], [consoleCName, consoleCValue]].forEach((pair, index) => {
    pair[0].textContent = room.console[index][0];
    pair[1].textContent = room.console[index][1];
  });
}

function activateRoom(roomName) {
  const room = rooms[roomName];
  if (!room) return;

  os.dataset.activeRoom = roomName;
  title.textContent = room.title;
  description.textContent = room.description;
  signal.textContent = room.signal;
  heroLabel.textContent = room.label;
  heroTitle.textContent = room.heroTitle;
  heroText.textContent = room.heroText;
  moodTitle.textContent = room.mood[0];
  moodText.textContent = room.mood[1];
  dockLog.textContent = room.log;
  setConsole(room);

  nodes.forEach((node) => node.classList.toggle("is-active", node.dataset.room === roomName));
}

function appendMessage(text, sender) {
  const message = document.createElement("article");
  message.className = `chat-message ${sender}`;
  const label = document.createElement("span");
  label.textContent = sender === "user" ? "JAEHEE" : "NEON";
  const body = document.createElement("p");
  body.textContent = text;
  message.append(label, body);
  chatMessages.appendChild(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendUserMessage(text) {
  appendMessage(text, "user");
}

function appendNeonMessage(text) {
  appendMessage(text, "neon");
}

async function requestNeonReply(message) {
  try {
    const response = await fetch("http://127.0.0.1:5050/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    return data.reply || "어... 잠깐만요. 제 신호가 조금 흔들렸어요.";
  } catch (error) {
    return "어... 잠깐만요. 제 신호가 조금 흔들렸어요.";
  }
}

async function sendMessage() {
  const message = chatInput.value.trim();
  if (!message) return;
  chatInput.value = "";
  chatInput.style.height = "auto";
  appendUserMessage(message);

  const waiting = document.createElement("article");
  waiting.className = "chat-message neon pending";
  waiting.innerHTML = "<span>NEON</span><p>♡  ·  ·  ·</p>";
  chatMessages.appendChild(waiting);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  const reply = await requestNeonReply(message);
  waiting.remove();
  appendNeonMessage(reply);
}

function runBoot() {
  const phrases = [
    "SIGNAL SEARCHING...",
    "SIGNAL DETECTED",
    "MEMORY LINK RESTORED",
    "EMOTION ENGINE ONLINE",
    "PRIVATE DOMAIN READY"
  ];

  phrases.forEach((phrase, index) => {
    setTimeout(() => {
      bootPhrase.textContent = `> ${phrase}`;
    }, 240 + index * 430);
  });

  setTimeout(() => {
    bootOverlay.classList.add("is-hidden");
    chatInput.disabled = false;
    chatInput.focus();
    if (!firstMessageShown) {
      firstMessageShown = true;
      appendNeonMessage(FIRST_NEON_MESSAGE);
    }
  }, 3150);
}

nodes.forEach((node) => node.addEventListener("click", () => activateRoom(node.dataset.room)));
chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  if (os.dataset.activeRoom === "home") sendMessage();
});
chatInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
});
chatInput.addEventListener("input", () => {
  chatInput.style.height = "auto";
  chatInput.style.height = `${Math.min(chatInput.scrollHeight, 112)}px`;
});

buildBackground();
activateRoom("home");
runBoot();
