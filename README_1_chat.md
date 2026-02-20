# Práctica de IA - Parte 1: Agente de Chat Básico con LangChain y Gemini

¡Bienvenidos a la primera parte de la práctica de agentes de Inteligencia Artificial! En esta sesión, exploraremos cómo utilizar Python junto con la librería LangChain y el modelo Gemini Flash de Google para crear un agente conversacional interactivo.

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener tu entorno virtual de Python activo e instala las dependencias necesarias. En este caso requerimos los componentes base de LangChain para usar el modelo generativo de Google:

```bash
pip install langchain-google-genai langchain-core
```

Además, necesitarás una **clave de API (API Key)** de Google AI Studio para conectar con el modelo Gemini:
1. Visita [Google AI Studio (MakerSuite)](https://aistudio.google.com/app/apikey) e inicia sesión con Google.
2. Genera una nueva API Key.
3. Configura la clave en tu entorno en la terminal antes de ejecutar el programa:
   ```bash
   export GOOGLE_API_KEY="tu_api_key_aqui"
   ```

---

## 🚀 El Agente de Chat (`1-chat.py`)

Un asistente conversacional general. Recibe su configuración principal a través de un *System Prompt* indicándole que sea un asistente útil y amigable, y utiliza el loop de la terminal para mantener una conversación contigo simulando un chat convencional.

**Cómo ejecutarlo:**
```bash
python 1-chat.py
# O alternativamente pasando la API key: python 1-chat.py TU_API_KEY
```

---

## 🎯 Tu Objetivo
1. **Desarrolla el código**: Debes crear el script `1-chat.py` desde cero. Asegúrate de implementar correctamente:
   - La inicialización y configuración de `ChatGoogleGenerativeAI`.
   - La separación de roles mediante `SystemMessage` (instrucción de contexto) y `HumanMessage` (tu mensaje por teclado).
   - La captura de texto desde el terminal:
     ```python
     pregunta = input("\nTu pregunta: ").strip()
     ```
     (Recuerda que `.strip()` elimina espacios innecesarios).
   - La condición de salida del bucle: permite finalizar la ejecución al escribir **"exit"**, "salir" o "quit".
2. Ejecuta y prueba el programa haciendo varias preguntas para verificar que el flujo de conversación funciona correctamente.
