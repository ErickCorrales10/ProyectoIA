from fastapi import APIRouter, HTTPException
from modelos import preguntas_padres
from base_datos import database
from esquemas import Pregunta
from typing import List

router = APIRouter()

@router.get("/preguntas/{nivel}", response_model=List[Pregunta])
async def obtener_preguntas(nivel: int):
    # Consultamos las preguntas para los padres del nivel especificado
    consulta = preguntas_padres.select().where(
        preguntas_padres.c.nivel == nivel
    )
    preguntas_registradas =  await database.fetch_all(consulta)
    
    if not preguntas_registradas:
        raise HTTPException(status_code=404, detail="No hay preguntas para este nivel.")
    
    return preguntas_registradas