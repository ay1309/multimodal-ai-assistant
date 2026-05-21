const clientId = crypto.randomUUID();
const wsUrl = `ws://${location.host}/ws/chat/${clientId}`;
const ws = new WebSocket(wsUrl);

const chatWindow = document.getElementById("chat-window");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const statusEl = document.getElementById("status");

let history = [];
let currentBubble = null;

ws.onopen = () => {
  statusEl.textContent = "Conectado";
  statusEl.className = "status online";
};

ws.onclose = () => {
  statusEl.textContent = "Desconectado";
  statusEl.className = "status offline";
};

ws.onmessage = ({ data }) => {
  const msg = JSON.parse(data);

  if (msg.type === "chunk") {
    currentBubble.textContent += msg.text;
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  if (msg.type === "done") {
    history.push({ role: "assistant", content: currentBubble.textContent });
    currentBubble = null;
    sendBtn.disabled = false;
  }

  if (msg.type === "error") {
    addMessage("Error: " + msg.message, "error");
    sendBtn.disabled = false;
  }
};

function addMessage(text, role) {
  const welcome = chatWindow.querySelector(".welcome");
  if (welcome) welcome.remove();

  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.textContent = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return div;
}

function sendMessage() {
  const text = input.value.trim();
  if (!text || sendBtn.disabled) return;

  addMessage(text, "user");
  history.push({ role: "user", content: text });
  input.value = "";
  input.style.height = "auto";

  currentBubble = addMessage("", "assistant");
  sendBtn.disabled = true;

  ws.send(JSON.stringify({ messages: history }));
}

sendBtn.onclick = sendMessage;

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = input.scrollHeight + "px";
});

document.getElementById("image-input").onchange = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  addMessage(`📎 ${file.name}`, "user");
  const form = new FormData();
  form.append("file", file);
  form.append("prompt", input.value || "Describe this image in detail.");
  input.value = "";
  const res = await fetch("/api/analyze-image", { method: "POST", body: form });
  const data = await res.json();
  addMessage(data.result, "assistant");
  history.push({ role: "user", content: `[image: ${file.name}]` });
  history.push({ role: "assistant", content: data.result });
};

document.getElementById("audio-input").onchange = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  addMessage(`🎙️ ${file.name}`, "user");
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("/api/transcribe", { method: "POST", body: form });
  const data = await res.json();
  addMessage(data.response, "assistant");
};