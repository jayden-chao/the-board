const chat = document.getElementById("chat");
const input = document.getElementById("input");
const sendBtn = document.getElementById("sendBtn");

const SESSION_KEY = "session_id";
let session_id = null;

window.addEventListener("load", initSession);

async function initSession() {

  const existingSessionId = localStorage.getItem(SESSION_KEY);

  if (existingSessionId) {
    session_id = existingSessionId;
    console.log("Using existing session:", existingSessionId);
    await loadHistory();
    return;
  }

  const response = await fetch("http://127.0.0.1:8000/sessions", {
    method: "POST"
  });

  const data = await response.json();
  session_id = data.id;
  localStorage.setItem(SESSION_KEY, data.id);
  console.log("Created new session:", data.id);

  await loadHistory();

}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});

async function sendMessage() {
  const message = input.value.trim();

  if (!message) {
    return;
  }

  const session_id = localStorage.getItem("session_id");

  addMessage("user", message);

  const response = await fetch(`http://127.0.0.1:8000/sessions/${session_id}/messages`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({content: message})
  });

  const data = await response.json();

  addMessage("board", data.content.raw);
  console.log("Board Reply:", data)

  input.value = ""

}

function addMessage(role, text) {

  const div = document.createElement("div");
  div.classList.add("message", role);
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;

}

async function loadHistory() {

  console.log("Loading history...");

  const session_id = localStorage.getItem("session_id");

  const response = await fetch(`http://127.0.0.1:8000/sessions/${session_id}/messages`, {
    method: "GET"
  })

  const data = await response.json();
  chat.innerHTML = "";

  console.log(data);
  data.forEach(message => {

    let text;

    if (typeof message.content === "string") {
      text = message.content;
    } else {
      text = message.content.raw;
    }

    console.log(`Logging ${message.role}: ${text}`);
    addMessage(message.role, text);
  });
}
