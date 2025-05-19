from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from transformers import pipeline
import html
import os

# from intents import preguntar_chatgpt

load_dotenv()

print('Erick')

app = FastAPI()
generator = pipeline('text-generation', model='gpt2-medium') # Cargar el modelo GPT-2 Small

@app.post("/")
async def handle_alexa(request: Request):
    respuesta_alexa = await request.json()
    
    print(f'Respuesta de Alexa: {respuesta_alexa}')
    
    tipo_peticion = respuesta_alexa["request"]['type']
    
    if tipo_peticion == "LaunchRequest":
        return JSONResponse(content={
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Hola! Bienvenido a Hablemos Juntos, donde te ayudaré a expresarte mejor."
                            " Dime ¿Sobre qué quieres que genere texto?"
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
                            "text": "Lo siento, no entendí la pregunta."
                                    "¿Puedes repetirla?"
                        },
                        "shouldEndSession": False
                    }
                })
                
        elif nombre_intent == "AMAZON.HelpIntent":
            return JSONResponse(content={
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Puedes pedirme que genere texto sobre cualquier cosa."
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
                        "text": "No entendí bien. ¿Puedes repetirlo por favor?"
                    },
                    "shouldEndSession": False
                }
            })
            
async def handle_pregunta_chatgpt(pregunta: str):
    try:
        print('generando texto')
        prompt = f'Pregunta: {pregunta}\nRespuesta:'
        
        generar_texto = generator(prompt, max_length=80, num_return_sequences=1, truncation=True)[0]['generated_text']
        print(f"La primera generación de texto es: {generar_texto}")
        respuesta_gpt = generar_texto.split("Respuesta:")[-1].split('\n')[0].strip()
        respuesta_gpt = html.escape(respuesta_gpt.replace('\n', " ").strip())
        
        print("\n\n\t\tLo que genera gpt-medium es:", respuesta_gpt, "\n\n")
        print(type(respuesta_gpt))
        
        respuesta_estatica = {
            "cual es la capital de francia": "La capital de Francia es París.",
            "quien descubrio america": "Cristóbal Colón descubrió América en 1492."
        }
        
        pregunta_lower = pregunta.lower().strip()
        respuesta = respuesta_estatica.get(pregunta_lower, "Aún no puedo responder eso con precisión.")
        
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
        
    except Exception as e:
        print("Error al generar texto con GPT-2 Small: ", e)
        return JSONResponse(content={
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Hubo un problema al generar texto."
                            " Intenta de nuevo más tarde."
                },
                "shouldEndSession": False
            }
        })