from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from intents import adivina_palabra

from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

""" # Modelo de datos
class Tarea(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str] = None
    completado: bool = False


# Lista simulando una base de datos
tareas: List[Tarea] = []

# Ruta para obtener todas las tareas
@app.get("/tareas", response_model=List[Tarea])
def obtener_tareas():
    return tareas

# Ruta para crear una nueva tarea
@app.post("/tareas", response_model=Tarea)
def crear_tarea(tarea: Tarea):
    tareas.append(tarea)
    return tarea

# Ruta para obtener una tarea por su ID
@app.get("/tareas/{tarea_id}", response_model=Tarea)
def obtener_tarea(tarea_id: int):
    for tarea in tareas:
        if tarea.id == tarea_id:
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# Ruta para marcar una tarea como completada
@app.put("/tareas/{tarea_id}/completar", response_model=Tarea)
def completar_tarea(tarea_id: int):
    for tarea in tareas:
        if tarea.id == tarea_id:
            tarea.completado = True
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
"""

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
                    "text": "Bienvenido a Habla Conmigo!! ¿Quieres jugar o escuchar las instrucciones?" 
                },
                "shouldEndSession": False
            }
        })
    
    elif tipo_peticion == "IntentRequest":
        nombre_intent = respuesta_alexa["request"]["intent"]["name"]

        if nombre_intent == "AdivinaLaPalabraIntent":
            return await adivina_palabra.handle_adivina_palabra()
        
        elif nombre_intent == "InstruccionesIntent":
            return await adivina_palabra.adivina_palabras_instrucciones()
        
        elif nombre_intent == "AMAZON.YesIntent":
            # Inicia el juego si el usuario dijo que sí después de las instrucciones
            return await adivina_palabra.handle_adivina_palabra()
        
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

