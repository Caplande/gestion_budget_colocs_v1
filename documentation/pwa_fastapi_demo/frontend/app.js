const API = "http://localhost:8000/api";

async function loadMessages() {
  const res = await fetch(`${API}/messages`);
  const data = await res.json();

  const ul = document.getElementById("messages");
  ul.innerHTML = "";

  data.forEach(m => {
    const li = document.createElement("li");
    li.textContent = m.text;
    ul.appendChild(li);
  });
}

async function sendMessage() {
  const input = document.getElementById("msgInput");
  const txt = input.value;

  await fetch(`${API}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: txt })
  });

  input.value = "";
  loadMessages();
}

// Charger les messages à l’ouverture
loadMessages();
