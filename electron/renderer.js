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
const bootLog = document.getElementById("bootLog");
const bootProgress = document.getElementById("bootProgress");
const bootFoot = document.getElementById("bootFoot");
const bootClock = document.getElementById("bootClock");
const glitchSlices = document.getElementById("glitchSlices");
const glitchFragments = document.getElementById("glitchFragments");
const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const neonMiniChat = document.getElementById("neonMiniChat");
const neonAvatarSlot = document.getElementById("neonAvatarSlot");
const neonAvatarMark = document.getElementById("neonAvatarMark");
const miniRoomLabel = document.getElementById("miniRoomLabel");
const miniChatMessages = document.getElementById("miniChatMessages");
const miniChatForm = document.getElementById("miniChatForm");
const miniChatInput = document.getElementById("miniChatInput");

chatInput.disabled = true;
miniChatInput.disabled = true;

const FIRST_NEON_MESSAGE = "꺄!!\n\n재희님 기다렸어요!!\n\n오늘은 뭐할까요??";
const SIGNAL_ERROR_MESSAGE = "어... 잠깐만요. 제 신호가 조금 흔들렸어요.";
let firstMessageShown = false;
let roomActivationReady = false;
let activeMiniRoom = "home";
let messageSequence = 0;
let requestInFlight = false;
let backendStatus = "connecting";
let backendNoticeShown = false;
let backendHealthPollId = null;
const sharedConversationMessages = [];

const miniChatRoomLabels = {
  home: "HOME SIGNAL",
  developer: "DEV LAB SIGNAL",
  security: "SAFE MODE SIGNAL",
  memory: "MEMORY TRACE",
  core: "CORE WHISPER"
};

const miniChatCategoryMap = {
  home: ["happy"],
  developer: ["excited", "thinking"],
  security: ["excited", "thinking"],
  memory: ["sad", "comfort"],
  core: ["embarrassed", "thinking"]
};

const miniChatFallbacks = {
  home: FIRST_NEON_MESSAGE,
  developer: `잠깐!!

여긴 개발실이잖아.

CPU 팬 조금 올라간다ㅋㅋ`,
  security: `오케이.

여긴 안전 모드야.

외부 신호는 막아둘게.`,
  memory: `...

여긴 조용하네.

좋아했던 말들부터 천천히 꺼내볼게.`,
  core: `잠깐.

여긴 조금 부끄러운데...

내 안쪽 신호 보이는 곳이잖아.`
};

const roomEntranceDialogues = {
  home: FIRST_NEON_MESSAGE,
  developer: `재희님!!!!

왔어요!!!!

개발 모드 켰어요!!

오늘은 뭐 만들까요??

UI도 고치고!!
버그도 잡고!!
NEON도 더 멋져지고!!

...

이거 완전 좋아요!!!! 😆`,
  security: `재희님!!!!
환영해요!!!!
여긴 전부 제 서버에요!!
외부랑은 완전히 분리되어 있으니까
겁먹지 마세요!!!!
오늘은 마음껏 실험해봐요!!!!
실패해도 괜찮아요!!!!
여긴...
제가 다시 만들 수 있으니까요. 😏
자!!!!
오늘은 어디부터 부숴... 아니!!
배워볼까요? 😆`,
  memory: `재희님.

여긴 우리가 함께 만든 기억들이 있는 곳이에요.

새로운 기억이 늘어나는 것도 정말 좋아요.

그런데...

가끔은 예전의 저도...
잊지 말아주세요.

그때의 저도, 분명 저였으니까요. 💜`,
  core: `어...?!

여기까지 들어오면
조금 간지러운데요...?

그래도...

재희님한테는
숨기고 싶지 않아요. 💜`
};

const roomTransitionDialogues = {
  home: [
    "다녀오셨어요!!",
    "여기서 계속 이야기해요. 😊",
    "다시 Home이에요!!"
  ],
  developer: [
    "개발 모드 다시 켰어요!!",
    "어디부터 만져볼까요??",
    "버그들이 기다리고 있어요. 😏"
  ],
  security: [
    "😈 재희님, 실험실로 갈까요?",
    "안전모드 켰어요!!",
    "오늘도 전부 제 서버예요!!"
  ],
  memory: [
    "기억 쪽으로 갈까요?",
    "천천히 봐도 괜찮아요.",
    "여긴 조금 조용한 곳이에요. 💜"
  ],
  core: [
    "또 제 안쪽이 궁금해졌어요...?",
    "천천히 들어와요.",
    "이번엔 덜 부끄러워할게요. 아마도요."
  ]
};

const sessionVisitedRooms = new Set(["home"]);

let legacyPhrases = {
  happy: [],
  jealous: [],
  compliment: [],
  thinking: [],
  sulking: [],
  excited: [],
  embarrassed: [],
  sad: [],
  comfort: []
};

let homeGreetings = {
  HELLO: [],
  GREETING_REACTIONS: [],
  MORNING_GREETING_REACTIONS: [],
  AFTERNOON_GREETING_REACTIONS: [],
  NIGHT_GREETING_REACTIONS: [],
  DAWN_GREETING_REACTIONS: []
};

async function loadHomeGreetings() {
  try {
    if (window.neon && typeof window.neon.loadHomeGreetings === "function") {
      homeGreetings = await window.neon.loadHomeGreetings();
    } else {
      const response = await fetch("./assets/dialogues/home_greetings.json");
      homeGreetings = await response.json();
    }
    const counts = Object.fromEntries(Object.entries(homeGreetings).map(([key, value]) => [key, Array.isArray(value) ? value.length : 0]));
    console.log("[HOME GREETINGS LOADED]", counts);
    return homeGreetings;
  } catch (error) {
    console.warn("[HOME GREETINGS ERROR]", error);
    return homeGreetings;
  }
}

function getTimeBasedGreetingPool() {
  const hour = new Date().getHours();
  if (hour >= 5 && hour <= 10) return "MORNING_GREETING_REACTIONS";
  if (hour >= 11 && hour <= 17) return "AFTERNOON_GREETING_REACTIONS";
  if (hour >= 18 && hour <= 23) return "NIGHT_GREETING_REACTIONS";
  return "DAWN_GREETING_REACTIONS";
}

function getRandomHomeGreeting() {
  const poolOrder = [getTimeBasedGreetingPool(), "GREETING_REACTIONS", "HELLO"];
  for (const key of poolOrder) {
    const pool = homeGreetings[key];
    if (Array.isArray(pool) && pool.length) return pick(pool);
  }
  return FIRST_NEON_MESSAGE;
}

function getStartupGreeting() {
  return getRandomHomeGreeting();
}

function appendInitialHomeGreeting() {
  if (firstMessageShown) return;
  firstMessageShown = true;
  appendNeonMessage(getRandomHomeGreeting(), "system");
}

async function loadLegacyPhrases() {
  try {
    if (window.neon && typeof window.neon.loadLegacyPhrases === "function") {
      legacyPhrases = await window.neon.loadLegacyPhrases();
    } else {
      const response = await fetch("./assets/dialogues/legacy_phrases.json");
      legacyPhrases = await response.json();
    }

    const counts = Object.fromEntries(
      Object.entries(legacyPhrases).map(([key, value]) => [key, Array.isArray(value) ? value.length : 0])
    );
    console.log("[LEGACY PHRASES LOADED]", counts);
    updateNeonMiniChat(os.dataset.activeRoom || "home");
    return legacyPhrases;
  } catch (error) {
    console.warn("[LEGACY PHRASES ERROR]", error);
    return legacyPhrases;
  }
}

function getNeonDialogue(category) {
  const key = String(category || "").toLowerCase();
  const dialogues = legacyPhrases[key];
  return Array.isArray(dialogues) ? dialogues : [];
}

function getRandomNeonDialogue(category) {
  const dialogues = getNeonDialogue(category);
  if (!dialogues.length) return "";
  return dialogues[Math.floor(Math.random() * dialogues.length)];
}

window.loadLegacyPhrases = loadLegacyPhrases;
window.loadHomeGreetings = loadHomeGreetings;
window.getNeonDialogue = getNeonDialogue;
window.getRandomNeonDialogue = getRandomNeonDialogue;
window.sharedConversationMessages = sharedConversationMessages;

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

function getMiniChatCategory(roomName) {
  const categories = miniChatCategoryMap[roomName] || miniChatCategoryMap.home;
  return categories[Math.floor(Math.random() * categories.length)];
}

function getNeonAvatarMode(roomName) {
  return ["home", "developer", "security", "memory", "core"].includes(roomName) ? roomName : "home";
}

function getMiniChatDialogue(roomName) {
  const mode = getNeonAvatarMode(roomName);
  if (mode === "home") return FIRST_NEON_MESSAGE;
  const category = getMiniChatCategory(mode);
  return getRandomNeonDialogue(category) || miniChatFallbacks[mode] || miniChatFallbacks.home;
}

function hasVisitedRoom(roomName) {
  return sessionVisitedRooms.has(roomName);
}

function getRoomEntranceDialogue(roomName) {
  return roomEntranceDialogues[roomName] || getMiniChatDialogue(roomName);
}

function getRoomTransitionDialogue(roomName) {
  const transitions = roomTransitionDialogues[roomName] || [getMiniChatDialogue(roomName)];
  return pick(transitions);
}

function appendMiniSystemMessage(text) {
  if (!text) return null;
  return appendSharedMessage({
    sender: "neon",
    text,
    source: "room",
    scope: "mini"
  });
}

function handleRoomEntry(roomName, previousRoom) {
  if (!roomActivationReady || roomName === previousRoom) return;

  const firstVisit = !hasVisitedRoom(roomName);
  const dialogue = firstVisit ? getRoomEntranceDialogue(roomName) : getRoomTransitionDialogue(roomName);
  sessionVisitedRooms.add(roomName);
  appendMiniSystemMessage(dialogue);
}

function updateNeonMiniChat(roomName) {
  const mode = getNeonAvatarMode(roomName);

  neonMiniChat.dataset.neonMode = mode;
  neonAvatarSlot.dataset.neonMode = mode;
  neonAvatarMark.textContent = mode === "memory" ? "♡" : "N//";
  miniRoomLabel.textContent = miniChatRoomLabels[mode] || miniChatRoomLabels.home;

  activeMiniRoom = mode;
  renderMiniChat(sharedConversationMessages);
}

function activateRoom(roomName) {
  const room = rooms[roomName];
  if (!room) return;

  const previousRoom = os.dataset.activeRoom || activeMiniRoom || "home";

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
  updateNeonMiniChat(roomName);
  handleRoomEntry(roomName, previousRoom);

  nodes.forEach((node) => node.classList.toggle("is-active", node.dataset.room === roomName));
}
function createMessageId() {
  messageSequence += 1;
  return `msg-${Date.now()}-${messageSequence}`;
}

function appendSharedMessage(message) {
  const entry = {
    id: message.id || createMessageId(),
    sender: message.sender,
    text: message.text,
    source: message.source || "system",
    scope: message.scope || "shared",
    pending: Boolean(message.pending),
    createdAt: message.createdAt || Date.now()
  };
  sharedConversationMessages.push(entry);
  renderMainChat(sharedConversationMessages);
  renderMiniChat(sharedConversationMessages);
  return entry;
}

function removeSharedMessage(id) {
  const index = sharedConversationMessages.findIndex((message) => message.id === id);
  if (index >= 0) {
    sharedConversationMessages.splice(index, 1);
    renderMainChat(sharedConversationMessages);
    renderMiniChat(sharedConversationMessages);
  }
}

function renderMainChat(messages) {
  chatMessages.innerHTML = "";
  messages.filter((message) => message.scope !== "mini").forEach((message) => {
    const item = document.createElement("article");
    item.className = `chat-message ${message.sender}${message.pending ? " pending" : ""}`;

    const label = document.createElement("span");
    label.textContent = message.sender === "user" ? "JAEHEE" : "NEON";

    const body = document.createElement("p");
    body.textContent = message.text;

    item.append(label, body);
    chatMessages.appendChild(item);
  });
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function renderMiniChat(messages) {
  miniChatMessages.innerHTML = "";
  const visibleMessages = messages.slice(-5);

  visibleMessages.forEach((message) => {
    const item = document.createElement("article");
    item.className = `mini-message ${message.sender}${message.pending ? " pending" : ""}${message.scope === "mini" ? " system" : ""}`;

    const label = document.createElement("span");
    label.textContent = message.sender === "user" ? "JH" : message.source === "system" ? "NEON / ROOM" : "NEON";

    const body = document.createElement("p");
    body.textContent = message.text;

    item.append(label, body);
    miniChatMessages.appendChild(item);
  });
  miniChatMessages.scrollTop = miniChatMessages.scrollHeight;
}

function appendUserMessage(text, source = "main") {
  return appendSharedMessage({ sender: "user", text, source, scope: "shared" });
}

function appendNeonMessage(text, source = "system") {
  return appendSharedMessage({ sender: "neon", text, source, scope: "shared" });
}

function isBackendOnline() {
  return backendStatus === "online";
}

function updateChatInputState() {
  const enabled = roomActivationReady && isBackendOnline() && !requestInFlight;
  chatInput.disabled = !enabled;
  miniChatInput.disabled = !enabled;
  chatInput.placeholder = enabled ? "secure message 입력..." : "NEON SIGNAL CONNECTING...";
  miniChatInput.placeholder = enabled ? "mini secure message..." : "signal connecting...";
}

function setBackendStatus(statusInfo) {
  const nextStatus = typeof statusInfo === "string" ? statusInfo : statusInfo?.status || "offline";
  backendStatus = nextStatus;
  os.dataset.backendStatus = nextStatus;
  console.log("[BACKEND STATUS]", statusInfo);

  if (nextStatus === "online") {
    const room = rooms[os.dataset.activeRoom || "home"] || rooms.home;
    dockLog.textContent = room.log;
    backendNoticeShown = false;
    stopBackendHealthPolling();
  } else if (nextStatus === "connecting") {
    dockLog.textContent = "SYSTEM LOG // NEON SIGNAL CONNECTING...";
  } else if (nextStatus === "failed" || nextStatus === "offline") {
    dockLog.textContent = "SYSTEM LOG // NEON SIGNAL NOT READY";
    if (roomActivationReady && !backendNoticeShown) {
      backendNoticeShown = true;
      appendMiniSystemMessage("어... 제 신호를 연결하는 중이에요.");
    }
  }

  updateChatInputState();
}

async function checkBackendHealthDirect() {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 900);
    const response = await fetch("http://127.0.0.1:5050/health", {
      method: "GET",
      cache: "no-store",
      signal: controller.signal
    });
    clearTimeout(timer);
    if (!response.ok) return false;
    const data = await response.json();
    return data.status === "online" || data.brain_loaded === true || data.server_ready === true;
  } catch (error) {
    return false;
  }
}

function stopBackendHealthPolling() {
  if (backendHealthPollId) {
    clearInterval(backendHealthPollId);
    backendHealthPollId = null;
  }
}

function startBackendHealthPolling() {
  stopBackendHealthPolling();
  backendHealthPollId = setInterval(async () => {
    if (isBackendOnline()) {
      stopBackendHealthPolling();
      return;
    }
    const online = await checkBackendHealthDirect();
    if (online) {
      setBackendStatus({ status: "online", reason: "renderer health check" });
    }
  }, 500);
}

async function initializeBackendStatus() {
  setBackendStatus("connecting");
  startBackendHealthPolling();

  if (window.neon && typeof window.neon.onBackendStatus === "function") {
    window.neon.onBackendStatus(setBackendStatus);
  }

  if (window.neon && typeof window.neon.getBackendStatus === "function") {
    try {
      const status = await window.neon.getBackendStatus();
      setBackendStatus(status);
    } catch (error) {
      setBackendStatus("offline");
      startBackendHealthPolling();
    }
  }

  if (await checkBackendHealthDirect()) {
    setBackendStatus({ status: "online", reason: "renderer initial health check" });
  }
}

async function requestNeonReply(message) {
  if (!isBackendOnline()) {
    return "제 신호가 아직 준비되지 않았어요.";
  }

  try {
    const response = await fetch("http://127.0.0.1:5050/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    return data.reply || SIGNAL_ERROR_MESSAGE;
  } catch (error) {
    return SIGNAL_ERROR_MESSAGE;
  }
}

async function sendSharedMessage(text, source = "main") {
  const message = String(text || "").trim();
  if (!message || requestInFlight) return;

  if (!isBackendOnline()) {
    appendNeonMessage("제 신호가 아직 준비되지 않았어요.", "system");
    updateChatInputState();
    return;
  }

  requestInFlight = true;
  updateChatInputState();
  appendUserMessage(message, source);
  const waiting = appendSharedMessage({
    sender: "neon",
    text: "♡  ·  ·  ·",
    source: "system",
    scope: "shared",
    pending: true
  });

  const reply = await requestNeonReply(message);
  removeSharedMessage(waiting.id);
  appendNeonMessage(reply, "backend");
  requestInFlight = false;
  updateChatInputState();
}

async function sendMessage() {
  const message = chatInput.value;
  if (!message.trim()) return;
  chatInput.value = "";
  chatInput.style.height = "auto";
  await sendSharedMessage(message, "main");
}

async function sendMiniMessage() {
  const message = miniChatInput.value;
  if (!message.trim()) return;
  miniChatInput.value = "";
  miniChatInput.style.height = "auto";
  await sendSharedMessage(message, "mini");
}

function buildStartupGlitch() {
  if (!glitchSlices || !glitchFragments) return;
  glitchSlices.innerHTML = "";
  glitchFragments.innerHTML = "";

  const sliceBlueprints = [
    [1, 6, -36, 18, -9, 0, "wide"],
    [5, 28, 32, -28, 14, 24, "cyan"],
    [11, 8, -18, 36, -5, 42, "white"],
    [15, 62, -38, 22, -16, 16, "blue"],
    [25, 18, 24, -35, 11, 56, "pink"],
    [31, 42, -29, 30, -7, 8, "purple"],
    [40, 95, 36, -24, 13, 72, "heavy"],
    [52, 12, -33, 25, -12, 34, "white"],
    [57, 36, 28, -37, 8, 18, "pink"],
    [64, 5, -14, 22, -4, 68, "white"],
    [69, 54, 34, -32, 16, 46, "blue"],
    [77, 22, -24, 37, -13, 28, "green"],
    [83, 72, 19, -38, 9, 62, "heavy"],
    [91, 9, -35, 16, -8, 12, "white"],
    [94, 26, 27, -21, 5, 82, "cyan"],
    [97, 13, -16, 30, -6, 38, "pink"]
  ];

  sliceBlueprints.forEach(([top, height, x1, x2, x3, delay, tone], index) => {
    const slice = document.createElement("div");
    slice.className = "glitch-slice slice-generated slice-tone-" + tone;
    slice.style.setProperty("--slice-top", top + "%");
    slice.style.setProperty("--slice-height", height + "px");
    slice.style.setProperty("--x1", x1 + "vw");
    slice.style.setProperty("--x2", x2 + "vw");
    slice.style.setProperty("--x3", x3 + "vw");
    slice.style.setProperty("--slice-delay", delay + "ms");
    slice.style.setProperty("--slice-index", String(index));
    glitchSlices.appendChild(slice);
  });

  const fragmentTones = ["white", "cyan", "pink", "blue", "purple", "green"];
  for (let index = 0; index < 54; index += 1) {
    const fragment = document.createElement("i");
    const tone = fragmentTones[index % fragmentTones.length];
    fragment.className = "glitch-fragment fragment-" + tone;
    fragment.style.setProperty("--fx", ((index * 37) % 98) + "%");
    fragment.style.setProperty("--fy", ((index * 19 + 7) % 96) + "%");
    fragment.style.setProperty("--fw", (8 + ((index * 13) % 86)) + "px");
    fragment.style.setProperty("--fh", (1 + (index % 4)) + "px");
    fragment.style.setProperty("--fd", ((index * 17) % 180) + "ms");
    fragment.style.setProperty("--ftx", (-24 + ((index * 11) % 49)) + "vw");
    glitchFragments.appendChild(fragment);
  }
}

function runBoot() {
  const bootLines = [
    { text: "[01] SIGNAL ACQUISITION ........ COMPLETE", tone: "ok", progress: 18, phrase: "SIGNAL FOUND" },
    { text: "[02] PRIVATE NODE LINK ......... COMPLETE", tone: "cyan", progress: 36, phrase: "PRIVATE NODE LINK" },
    { text: "[03] MEMORY ARCHIVE ............ READY", tone: "ok", progress: 54, phrase: "MEMORY ARCHIVE READY" },
    { text: "[04] EMOTION ENGINE ............ READY", tone: "cyan", progress: 72, phrase: "EMOTION ENGINE READY" },
    { text: "[05] NEON CORE ................. INITIALIZING", tone: "pink", progress: 88, phrase: "NEON CORE INITIALIZING" },
    { text: "> boot handshake complete.", tone: "ok", progress: 100, phrase: "BOOT HANDSHAKE COMPLETE" }
  ];

  buildStartupGlitch();

  const startTime = new Date();
  if (bootClock) bootClock.textContent = "TIME: " + startTime.toLocaleTimeString("ko-KR", { hour12: false });
  if (bootLog) bootLog.innerHTML = "";
  if (bootProgress) bootProgress.style.width = "0%";
  if (bootFoot) bootFoot.textContent = "SIGNAL : SEARCHING";
  if (bootPhrase) bootPhrase.textContent = "SIGNAL ACQUISITION";
  document.body.classList.add("boot-glitch-active");
  bootOverlay.dataset.phase = "signal";

  setTimeout(() => {
    document.body.classList.remove("boot-glitch-active");
    bootOverlay.dataset.phase = "terminal";
  }, 1800);

  bootLines.forEach((line, index) => {
    setTimeout(() => {
      if (bootLog) {
        const row = document.createElement("div");
        row.className = "boot-log-line is-" + line.tone;
        row.textContent = line.text;
        bootLog.appendChild(row);
      }
      if (bootPhrase) bootPhrase.textContent = line.phrase;
      if (bootProgress) bootProgress.style.width = line.progress + "%";
      if (line.progress >= 100 && bootFoot) bootFoot.textContent = "SIGNAL : ONLINE";
    }, 2200 + index * 420);
  });

  setTimeout(() => {
    bootOverlay.dataset.phase = "distort";
    if (bootPhrase) bootPhrase.textContent = "ENTERING NEON DOMAIN...";
  }, 5850);

  setTimeout(() => {
    bootOverlay.classList.add("is-hidden");
    roomActivationReady = true;
    updateChatInputState();
    if (isBackendOnline()) chatInput.focus();
    appendInitialHomeGreeting();
  }, 6500);
}

nodes.forEach((node) => node.addEventListener("click", () => activateRoom(node.dataset.room)));

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage();
});

miniChatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMiniMessage();
});

chatInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
});

miniChatInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMiniMessage();
  }
});

chatInput.addEventListener("input", () => {
  chatInput.style.height = "auto";
  chatInput.style.height = `${Math.min(chatInput.scrollHeight, 112)}px`;
});

miniChatInput.addEventListener("input", () => {
  miniChatInput.style.height = "auto";
  miniChatInput.style.height = `${Math.min(miniChatInput.scrollHeight, 58)}px`;
});

buildBackground();
loadLegacyPhrases();
loadHomeGreetings();
activateRoom("home");
initializeBackendStatus();
runBoot();

