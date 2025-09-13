# 22310190_Adquirir_Conocimiento
Práctica 2 de Sistemas Expertos 

![alt text](image.png)

“Este módulo de adquisición de conocimiento está implementado en Python, un lenguaje ampliamente usado en la industria tecnológica, incluyendo empresas como Intel, para tareas de IA, automatización y manejo de datos. La aplicación puede evolucionar a un chatbot web integrable con bases de datos o modelos de lenguaje, lo que conecta con las tendencias actuales en sistemas expertos e inteligencia artificial.”


# Chatbot con Módulo de Adquisición de Conocimiento — Versión Web (Flask)
Resumen / Elevator Pitch (para Intel)

**Concepto**: Un prototipo de sistema experto tipo chatbot web implementado en Python/Flask que incorpora un módulo de adquisición de conocimiento. Cuando el bot no encuentra una respuesta adecuada, solicita al usuario una respuesta que luego guarda en su base de conocimiento (JSON). Esto demuestra habilidades en: ingeniería de software, NLP básico, backend web, persistencia de datos y diseño para escalabilidad — todas competencias relevantes para roles en Intel (IA, MLOps, Ingeniería de Software).

Por qué es relevante para Intel: Intel trabaja con plataformas de datos, modelos ML y soluciones de automatización; este proyecto es una prueba de concepto para un knowledge ingestion loop (bucle de ingestión de conocimiento) que puede escalar para integrarse con bases de datos empresariales, pipelines ETL, motores de búsqueda semántica y modelos de lenguaje a nivel de producción.

## Características clave del prototipo

- Interfaz web sencilla y profesional (HTML + CSS).

- Persistencia de conocimiento en conocimiento.json (formato legible y portable).

- Matching básico: coincidencia exacta y normalizada (lowercase y strip).

- Ruta de aprendizaje: si no existe match, el bot pide una respuesta y la guarda.

- API REST mínima para integraciones futuras (endpoint /api/query).

- Preparado para desplegar en Render / Heroku / Docker.

## Wireframe e interfaz 

1. Barra superior con título: Intel-style Knowledge Chat

2. Panel izquierdo: lista de temas o atajos ("Saludar", "Soporte Intel", "FAQ técnica") — opcional

3. Panel principal: ventana de chat (burbujas claras, texto legible)

4. Entrada de texto abajo + botón "Enviar" + botón "Enseñar" (aparece cuando se solicita aprendizaje)

5. Pequeño banner: "Aprendido: n entradas" (contador de la base de conocimiento)
