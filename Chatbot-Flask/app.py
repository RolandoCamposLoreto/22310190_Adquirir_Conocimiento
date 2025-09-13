from flask import Flask, render_template, request, jsonify
with open(DB_FILE, 'r', encoding='utf-8') as f:
conocimiento = json.load(f)
else:
# precargadas
conocimiento = {
'hola': '¡Hola! ¿Cómo estás?',
'como estas': 'Estoy bien, gracias. ¿Y tú?',
'de que te gustaria hablar': 'Podemos hablar de tecnología, de Intel o de lo que quieras.'
}


# Util: guardar
def guardar_conocimiento():
with open(DB_FILE, 'w', encoding='utf-8') as f:
json.dump(conocimiento, f, ensure_ascii=False, indent=4)


# Normalizar texto para matching
def normalizar(texto: str) -> str:
return ' '.join(texto.lower().strip().split())


@app.route('/')
def index():
return render_template('index.html', aprendido=len(conocimiento))


# Endpoint para consultas desde la UI
@app.route('/query', methods=['POST'])
def query():
data = request.json or {}
texto = data.get('texto', '')
texto_norm = normalizar(texto)


if texto_norm in conocimiento:
return jsonify({'status': 'ok', 'respuesta': conocimiento[texto_norm], 'aprender': False})
else:
# No encontró match
prompt = ("No conozco esa respuesta aún. "
"¿Qué debería responder si alguien me pregunta eso?")
# Devolver estado para que la UI muestre el formulario de enseñanza
return jsonify({'status': 'learn', 'respuesta': prompt, 'aprender': True})


# Endpoint para enseñar nueva respuesta
@app.route('/teach', methods=['POST'])
def teach():
data = request.json or {}
pregunta = normalizar(data.get('pregunta', ''))
respuesta = data.get('respuesta', '').strip()


if not pregunta or not respuesta:
return jsonify({'status': 'error', 'mensaje': 'Pregunta o respuesta vacía'}), 400


conocimiento[pregunta] = respuesta
guardar_conocimiento()
return jsonify({'status': 'ok', 'mensaje': 'Aprendido', 'aprender': False, 'apren_count': len(conocimiento)})


# API REST simple (útil para integraciones)
@app.route('/api/query', methods=['POST'])
def api_query():
return query()


if __name__ == '__main__':
app.run(debug=True, port=5000)