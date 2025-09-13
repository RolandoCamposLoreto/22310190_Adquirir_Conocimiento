const chatbox = document.getElementById('chatbox');
let pendingQuestion = null;


function appendMessage(text, who='bot'){
const div = document.createElement('div');
div.className = 'message ' + (who === 'user' ? 'user' : 'bot');
div.innerText = text;
chatbox.appendChild(div);
chatbox.scrollTop = chatbox.scrollHeight;
}


btnEnviar.onclick = async () => {
const txt = texto.value.trim();
if (!txt) return;
appendMessage(txt, 'user');
texto.value = '';


const res = await fetch('/query', {
method: 'POST',
headers: {'Content-Type': 'application/json'},
body: JSON.stringify({texto: txt})
});
const data = await res.json();
appendMessage(data.respuesta, 'bot');


if (data.aprender) {
// mostrar boton enseñar y recordar pregunta
pendingQuestion = txt;
btnAprender.style.display = 'inline-block';
} else {
pendingQuestion = null;
btnAprender.style.display = 'none';
}
}


btnAprender.onclick = async () => {
const respuesta = prompt('¿Qué debería responder el chatbot?');
if (!respuesta) return;
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
// actualizar badge (opcional: recargar o hacer fetch extra)
location.reload();
} else {
alert('Error al guardar: ' + (data.mensaje || ''));
}
}


// enviar con Enter
texto.addEventListener('keydown', (e) => {
if (e.key === 'Enter') btnEnviar.click();
});