from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import openai
import os

# Importar el intent
from intents import preguntar_chatgpt

#Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
@app.post("/")
async def handle_alexa(request: Request):
    print(f'La clave de la API es:{openai.api_key}')
    respuesta_alexa = await request.json()
    print(f'Respuesta de Alexa: {respuesta_alexa}')

    tipo_peticion = respuesta_alexa["request"]['type']

    if tipo_peticion == 'LaunchRequest':
        return JSONResponse(content={
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "¡Hola! Bienvenido a Hablemos Juntos, donde te ayudaré a expresarte mejor. "
                            "Dime ¿Cuál es tu nombre?"
                },
                "shouldEndSession": False
            }
        })
    
    elif tipo_peticion == "IntentRequest":
        intent = respuesta_alexa["request"]["intent"]
        nombre_intent = intent["name"]

        if nombre_intent == "PreguntaChatgptIntent":
            pregunta_usuario = intent["slots"]["pregunta"]["value"]
            return await preguntar_chatgpt.handle_pregunta_chatgpt(pregunta_usuario)

    else:
        return JSONResponse(content={
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "No entendí bien. ¿Puedes repetirlo por favor?"
                },
                "shoulddEndSession": False
            }
        })