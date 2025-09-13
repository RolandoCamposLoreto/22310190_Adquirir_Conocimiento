const chatbox = document.getElementById('chatbox');
const texto = document.getElementById('texto');
const btnEnviar = document.getElementById('enviar');
const btnAprender = document.getElementById('aprender');
let pendingQuestion = null;

function appendMessage(text, who='bot'){
  const div = document.createElement('div');
  div.className = 'message ' + (who === 'user' ? 'user' : 'bot');
  div.innerText = text;
  chatbox.appendChild(div);
  chatbox.scrollTop = chatbox.scrollHeight;
}

// Enviar mensaje al chatbot
btnEnviar.onclick = async () => {
  const txt = texto.value.trim();
  if (!txt) return;

  appendMessage(txt, 'user');
  texto.value = '';

  try {
    const res = await fetch('/query', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({texto: txt})
    });
    const data = await res.json();
    appendMessage(data.respuesta, 'bot');

    if (data.aprender){
      pendingQuestion = txt;
      btnAprender.style.display = 'inline-block';
    } else {
      pendingQuestion = null;
      btnAprender.style.display = 'none';
    }
  } catch (err) {
    appendMessage('Error al contactar al servidor.', 'bot');
    console.error(err);
  }
};

// Enseñar nueva respuesta
btnAprender.onclick = async () => {
  if (!pendingQuestion) return;
  const respuesta = prompt('¿Qué debería responder el chatbot?');
  if (!respuesta) return;

  try {
    const res = await fetch('/teach', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({pregunta: pendingQuestion, respuesta})
    });
    const data = await res.json();
    if (data.status === 'ok'){
      appendMessage(respuesta, 'user');
      appendMessage('¡Gracias! He aprendido algo nuevo 🎓', 'bot');
      btnAprender.style.display = 'none';
      pendingQuestion = null;
      location.reload(); // actualiza badge de entradas
    } else {
      alert('Error al guardar: ' + (data.mensaje || ''));
    }
  } catch (err) {
    alert('Error al conectar con el servidor.');
    console.error(err);
  }
};

// Enviar con Enter
texto.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') btnEnviar.click();
});
