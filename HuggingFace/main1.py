from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import requests
import html
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
print(f"Token cargado: {HF_TOKEN}")

cliente = InferenceClient(
    # model="HuggingFaceH4/zephyr-7b-beta",
    model="meta-llama/Llama-3.1-8B-Instruct",
    token=HF_TOKEN
)

app = FastAPI()

def preguntar_huggingface(pregunta: str) -> str:
    try:
        completion = cliente.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": pregunta
                }
            ],
            max_tokens=1024,
            temperature=0.7,
            top_p=0.95
        )
        respuesta = completion.choices[0].message.content
        return respuesta.strip()
    
    except Exception as e:
        print("Error al consultar Hugging Face:", e)
        return "Lo siento, no puedo generar una respuesta en este momento."
    
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