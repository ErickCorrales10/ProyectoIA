from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import requests
import html
from huggingface_hub import InferenceClient
import asyncio
import time

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
print(f"Token cargado: {HF_TOKEN}")

cliente = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    # model="meta-llama/Llama-3.1-8B-Instruct",
    # model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    token=HF_TOKEN
)

app = FastAPI()

def preguntar_huggingface(pregunta: str) -> str:
    try:
        inicio = time.time()
        completion = cliente.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": pregunta
                }
            ],
            max_tokens=512,
            temperature=0.7,
            top_p=0.95
        )
        fin = time.time()
        print(f'Tiempo de respuesta: {fin - inicio}.2f segundos')
        
        respuesta = completion.choices[0].message.content
        return respuesta.strip()
    
    except Exception as e:
        print("Error al consultar Hugging Face:", e)
        return "Lo siento, no puedo generar una respuesta en este momento."
    
async def preguntar_huggingface_asyn(pregunta: str) -> str:
    return await asyncio.to_thread(preguntar_huggingface, pregunta)
    
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
    respuesta = await preguntar_huggingface_asyn(pregunta)
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