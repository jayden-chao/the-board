const chat = document.getElementById("chat");
const input = document.getElementById("input");
const sendBtn = document.getElementById("sendBtn");
const contrarian = document.getElementById("agent-contrarian");
const supporter = document.getElementById("agent-supporter");
let perspective = "supporter";

input.disabled = true;
sendBtn.disabled = true;

const SESSION_KEY = "session_id";
let session_id = null;

window.addEventListener("load", initSession);

async function initSession() {

  const existingSessionId = localStorage.getItem(SESSION_KEY);

  if (existingSessionId) {
    session_id = existingSessionId;
    console.log("Using existing session:", existingSessionId);
    await loadHistory();
    input.disabled = false;
    sendBtn.disabled = false;
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

  input.disabled = false;
  sendBtn.disabled = false;

}


sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
});


document.querySelectorAll("#agents img").forEach((img) => {
  img.addEventListener("click", () => {

    const isActive = img.classList.contains("active");

    document.querySelectorAll("#agents img").forEach((other) => {
      other.classList.remove("active");
    });

    if (!isActive) {
      img.classList.add("active");
    }

    if (contrarian.classList.contains("active")) {
      perspective = "contrarian";
    } else if (supporter.classList.contains("active")) {
      perspective = "supporter";
    }

    updatePerspective(perspective)

  });
});


async function updatePerspective(perspective) {
  
  const response = await fetch("http://127.0.0.1:8000/perspective", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({value: perspective})
  })
}


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

  input.value = "";

}

function addMessage(role, text) {

  const div = document.createElement("div");
  console.log("creating div");
  div.classList.add("message", role);
  div.textContent = text;
  chat.appendChild(div);
  console.log("appending div");
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
