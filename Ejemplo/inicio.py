from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from intents import adivina_palabra, sonidos_finales, sonidos_iniciales


app = FastAPI()

@app.post("/")
async def handle_alexa(request: Request):
    respuesta_alexa = await request.json()
    print(f"Solicitud de Alexa: {respuesta_alexa}")

    tipo_peticion = respuesta_alexa["request"]["type"]

    # Abrir la skill
    if tipo_peticion == "LaunchRequest":
        return JSONResponse(content={
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "¡Hola! Bienvenido a Habla Conmigo, donde te ayudaré a expresarte mejor. "
                    "Empezamos con el primer nivel, y te acompañare en cada paso. "
                    "¿Estás listo para comenzar?" 
                },
                "shouldEndSession": False
            }
        })
    
    # Seleccionar un ejercicio
    elif tipo_peticion == "IntentRequest":
        nombre_intent = respuesta_alexa["request"]["intent"]["name"]

        print(f'El nombre del intent es: {nombre_intent}')

        if nombre_intent == "AdivinaLaPalabraIntent":
            return await adivina_palabra.handle_adivina_palabra()
        
        elif nombre_intent == "InstruccionesIntent":
            return await adivina_palabra.adivina_palabras_instrucciones()
        
        elif nombre_intent == "AMAZON.YesIntent":
            # Inicia el juego si el usuario dijo que sí después de las instrucciones
            return await adivina_palabra.handle_adivina_palabra()
        
        elif nombre_intent == "ResponderPalabraIntent":
            valor_slot = respuesta_alexa["request"]["intent"]["slots"]["respuesta_palabra"]["value"].lower()
            palabra_correcta = respuesta_alexa["session"]["attributes"]["palabra_correcta"]
            return await adivina_palabra.verificar_palabra(valor_slot, palabra_correcta)
        
        elif nombre_intent == "AMAZON.StartOverIntent":
            return JSONResponse(content={
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "¡Hola! Bienvenido a Habla Conmigo, donde te ayudaré a expresarte mejor. "
                                "Empezamos con el primer nivel, y te acompañare en cada paso. "
                                "¿Estás listo para comenzar?"
                    },
                    "shouldEndSession": False
                }
            })
        
        elif nombre_intent == "SonidosInicialesIntent":
            return await sonidos_iniciales.handle_sonidos_iniciales()

        else:
            # Intent no reconocido
            return JSONResponse(content={
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "No reconozco esa opción. Por favor, intenta otra vez."
                    },
                    "shouldEndSession": False
                }
            })