from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import requests
import html

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
print(f"Token cargado: {HF_TOKEN}")

app = FastAPI()

def preguntar_huggingface(pregunta: str) -> str:
    # API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    # API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom-560m"
    # API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    prompt = f"Responde en español de forma concisa y clara:\nPregunta: {pregunta}\nRespuesta:"
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=20)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            respuesta = data[0]["generated_text"]
            respuesta_limpia = respuesta.split("Respuesta:")[-1].strip()
            return html.escape(respuesta_limpia)
        else:
            print("Respuesta inesperada de Hugging Face:", data)
            return "El modelo aún no está listo. Intenta en unos segundos."
    
    except Exception as e:
        print("Error al preguntar a Hugging Face:", e)
        return "Lo siento, no puedo generar una respuesta."
    
@app.post("/")
async def handle_alexa(request: Request):
    respuesta_alexa = await request.json()
    print(f"\nRespuesta de Alexa: {respuesta_alexa}\n")
    
    tipo_peticion = respuesta_alexa["request"]["type"]
    
    if tipo_peticion == "LaunchRequest":
        return JSONResponse(content={
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Hola! Bienvenido a Hablemos Juntos. "
                            "¿Sobre qué te gustaría hablar hoy?"
                },
                "shouldEndSession": False
            }
        })
        
    elif tipo_peticion == "IntentRequest":
        intent = respuesta_alexa["request"]["intent"]
        nombre_intent = intent["name"]
        
        if nombre_intent == "PreguntaChatgptIntent":
            try:
                pregunta_usuario = intent["slots"]["pregunta"]["value"]
                return await handle_pregunta_chatgpt(pregunta_usuario)
            
            except KeyError:
                return JSONResponse(content={
                    "version": "1.0",
                    "response": {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": "No entendí la pregunta. "
                                    "¿Puedes repetirla por favor?"
                        },
                        "shouldEndSession": False
                    }
                })
                
    else:
        return JSONResponse(content={
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "No reconocí esa solicitud. Inténtalo otra vez."
                },
                "shouldEndSession": False
            }
        })
        
async def handle_pregunta_chatgpt(pregunta: str):
    print("Generando respuesta desde Hugging Face para la pregunta:", pregunta)
    respuesta = preguntar_huggingface(pregunta)
    print("Respuesta generada:", respuesta)
    
    return JSONResponse(content={
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": respuesta
            },
            "shouldEndSession": False
        }
    })