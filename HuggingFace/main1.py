from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import requests
import html
from huggingface_hub import InferenceClient
import asyncio
import time
import escucha_palabra
import sonidos_iniciales
from base_datos import database, metadata, engine
from modelos import chat_preguntas
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from sqlalchemy import insert

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
print(f"Token cargado: {HF_TOKEN}")

cliente = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    # model="meta-llama/Llama-3.1-8B-Instruct",
    # model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    token=HF_TOKEN
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Conectando a la base de datos....")
    await database.connect()
    print('Conectado a la base de datos')

    yield
    print("Desconectado de la base de datos...")
    await database.disconnect()
    
    
app = FastAPI(
    title="Skill Afasia/Disfasia",
    lifespan=lifespan
)

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
                            "Puedes preguntarme lo que quieras o jugar alguno de los juegos que tengo para ti. "
                            "¿Qué deseas hacer?"
                },
                "shouldEndSession": False
            }
        })
        
    elif tipo_peticion == "IntentRequest":
        intent = respuesta_alexa["request"]["intent"]
        nombre_intent = intent["name"]
        
        if nombre_intent == "PreguntaChatIntent":
            try:
                pregunta_usuario = intent["slots"]["pregunta"]["value"]
                return await handle_pregunta_chat(pregunta_usuario)
            
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
                
        elif nombre_intent == "EscuchaPalabraIntent":
            try:
                return await escucha_palabra.handle_escucha_palabra()
            except Exception as e:
                print(f'Error al  manejar el juego: {e}')
                return JSONResponse(content={
                    "version": "1.0",
                    "response": {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": "Lo siento, no puedo iniciar el juego en este momento."
                        },
                        "shouldEndSession": False
                    }
                })
                
        elif nombre_intent == "InstruccionesEscuchaPalabraIntent":
            try:
                return await escucha_palabra.escucha_palabras_instrucciones()
            except Exception as e:
                print(f'Error al manejar las instrucciones: {e}')
                return JSONResponse(content={
                    "version": "1.0",
                    "response": {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": "Lo siento, no puedo proporcionar las instrucciones en este momento."
                        },
                        "shouldEndSession": False
                    }
                })
                
        elif nombre_intent == "ResponderPalabraIntent":
            try:
                valor_usuario = intent["slots"]["palabra"]["value"].lower()
                palabra_correcta = respuesta_alexa["session"]["attributes"]["palabra_correcta"]
                return await escucha_palabra.verificar_palabra(valor_usuario, palabra_correcta)
            except Exception as e:
                print(f'Error al verificar la palabra: {e}')
                return JSONResponse(content={
                    "version": "1.0",
                    "response": {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": "No entendí la respuesta. "
                                    "¿Puedes repetirla por favor?"
                        },
                        "shouldEndSession": False
                    }
                })
                
        elif nombre_intent == "SonidosInicialesIntent":
            try:
                return await sonidos_iniciales.handle_sonidos_iniciales()
            except Exception as e:
                print(f'Error al manejar los sonidos iniciales: {e}')
                return JSONResponse(content={
                    "version": "1.0",
                    "response": {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": "Lo siento, no puedo iniciar el juego de sonidos iniciales en este momento."
                        },
                        "shouldEndSession": False
                    }
                })
                
        elif nombre_intent == "ResponderSonidosInicialesIntent":
            try:
                valor_usuario = intent["slots"]["palabra_escuchada"]["value"].lower()
                palabra_correcta = respuesta_alexa["session"]["attributes"]["palabra_correcta"]
                return await sonidos_iniciales.verificar_palabra(valor_usuario, palabra_correcta)
            except Exception as e:
                print(f'Error al verificar la palabra: {e}')
                return JSONResponse(content={
                    "version": "1.0",
                    "response": {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": "No entendí la respuesta. "
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

async def handle_pregunta_chat(pregunta: str):
    print("Generando respuesta desde Hugging Face para la pregunta:", pregunta)
    respuesta = await preguntar_huggingface_asyn(pregunta)
    print("Respuesta generada:", respuesta)
    
    try:
        query = insert(chat_preguntas).values(
            pregunta=pregunta,
            respuesta=respuesta,
            fecha_creacion=datetime.now(timezone.utc)
        )
        await database.execute(query)
        print("Pregunta y respuesta insertadas en la base de datos.")
    except Exception as e:
        print("Error al insertar en la base de datos:", e)
    
    
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