from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/alexa")
async def control_alexa(request: Request):
    data = await request.json()
    intent = data.get("request", {}).get("intent", {}).get("name")

    # Lógica básica: responder a un intent
    if intent == "EjercicioIntent":
        respuesta = {
            "version": "1.0",
            "response": {
                "shouldEndSession": False,
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Vamos a comenzar un ejercicio de sonidos. Dime qué palabra escuchas: casa o taza."
                }
            }
        }

        return JSONResponse(content=respuesta)
    
    # Fallback
    return JSONResponse(content={
        "version": "1.0",
        "response": {
            "shouldEndSession": True,
            "outputSpeech": {
                "type": "PlainText",
                "text": "Lo sieto, no entendí tu solicitud"
            }
        }
    })