from flask import Flask, render_template, request, jsonify
import json
import os
import unicodedata
import re
from difflib import get_close_matches
import random

DB_FILE = 'conocimiento.json'
app = Flask(__name__)

# Cargar o inicializar base de conocimiento
if os.path.exists(DB_FILE):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        conocimiento = json.load(f)
else:
    # Base inicial con listas de respuestas
    conocimiento = {
        "hola": ["¡Hola! ¿Cómo estás?", "¡Hey! ¿Qué tal?", "¡Hola! Me alegra verte por aquí."],
        "buenos dias": ["¡Buenos días! ¿Cómo te encuentras hoy?", "¡Buen día! Espero que tengas un excelente día."],
        "buenas tardes": ["¡Buenas tardes! ¿Qué tal tu día?", "¡Buenas tardes! ¿Cómo va todo?"],
        "buenas noches": ["¡Buenas noches! Que descanses.", "¡Buenas noches! ¿Cómo estuvo tu día?"],
        "como estas": ["Estoy bien, gracias. ¿Y tú?", "Todo perfecto, ¿y tú?", "¡Muy bien! ¿Y tú?"],
        "que tal": ["Todo bien, gracias. ¿Y tú?", "¡Hola! ¿Qué tal todo?", "¡Qué gusto verte! Todo bien?"],
        "hey": ["¡Hey! ¿Cómo va todo?", "¡Hola! ¿Qué onda?", "¡Hey! Me alegra verte."],
        "holaaa": ["¡Hola! Me alegra verte por aquí.", "¡Holaaa! ¿Cómo estás?", "¡Hey! Qué bueno verte."],
        "de que te gustaria hablar": ["Podemos hablar de tecnología, de Intel o de lo que quieras.", "Hablemos de lo que te interese, tecnología, ciencia o curiosidades."],
        "que haces": ["Estoy aquí para conversar contigo y aprender cosas nuevas.", "Solo chateo contigo y aprendo cosas nuevas."],
        "como va todo": ["Todo va muy bien, gracias. ¿Y tú?", "Muy bien, gracias por preguntar.", "¡Todo perfecto!"]
    }

# Guardar conocimiento
def guardar_conocimiento():
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(conocimiento, f, ensure_ascii=False, indent=4)

# Normalizar texto: minúsculas, quitar acentos, signos y espacios extras
def normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    texto = re.sub(r'[^\w\s]', '', texto)
    texto = ' '.join(texto.split())
    return texto

# Buscar conocimiento con coincidencia aproximada y respuestas aleatorias
def buscar_conocimiento(texto: str):
    texto_norm = normalizar(texto)
    if texto_norm in conocimiento:
        resp = conocimiento[texto_norm]
        if isinstance(resp, list):
            return random.choice(resp)
        return resp
    # Coincidencia aproximada: tomar aleatoriamente entre matches
    matches = get_close_matches(texto_norm, conocimiento.keys(), n=3, cutoff=0.6)
    if matches:
        elegido = random.choice(matches)
        resp = conocimiento[elegido]
        if isinstance(resp, list):
            return random.choice(resp)
        return resp
    return None

@app.route('/')
def index():
    return render_template('index.html', aprendido=len(conocimiento))

@app.route('/query', methods=['POST'])
def query():
    data = request.json or {}
    texto = data.get('texto', '')
    respuesta = buscar_conocimiento(texto)

    if respuesta:
        return jsonify({'status': 'ok', 'respuesta': respuesta, 'aprender': False})
    else:
        prompt = "No conozco esa respuesta aún. ¿Qué debería responder si alguien me pregunta eso?"
        return jsonify({'status': 'learn', 'respuesta': prompt, 'aprender': True})

@app.route('/teach', methods=['POST'])
def teach():
    data = request.json or {}
    pregunta = normalizar(data.get('pregunta', ''))
    respuesta = data.get('respuesta', '').strip()

    if not pregunta or not respuesta:
        return jsonify({'status': 'error', 'mensaje': 'Pregunta o respuesta vacía'}), 400

    # Guardar respuesta nueva como lista (para permitir variaciones futuras)
    conocimiento[pregunta] = [respuesta]
    guardar_conocimiento()
    return jsonify({'status': 'ok', 'mensaje': 'Aprendido', 'aprender': False, 'apren_count': len(conocimiento)})

@app.route('/api/query', methods=['POST'])
def api_query():
    return query()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
