from fastapi.responses import JSONResponse
import openai 
import os

async def handle_pregunta_chatgpt(pregunta: str):
    try:
        respuesta = openai.chat.completions.create(
            model = "gpt-4.1-mini",
            messages = [
                {"role": "system", "content": "Eres un asistente amable."},
                {"role": "user", "content": pregunta}
            ]
        )

        # respuesta_chatgpt = f"Pues tengo que esperar para responder a tu pregunta...{pregunta}"

        respuesta_chatgpt = respuesta.choices[0].message.content

        return JSONResponse(content={
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": respuesta_chatgpt                
                },
                "shouldEndSession": False
            }
        })
    
    except Exception as e:
        print("Error al llamar a OpenAI: ", e)
        return JSONResponse(content={
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Hubo un problema al procesar tu respuesa. Intenta de nuevo más tarde."                
                },
                "shouldEndSession": False
            }
        })
