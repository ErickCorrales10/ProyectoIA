from fastapi import APIRouter, HTTPException
from base_datos import database
from modelos import ejercicios
from esquemas import Ejercicio
from typing import List

# Ejercicios predefinidos por nivel y tipo
router = APIRouter()

@router.get("/ejercicios/{nivel}", response_model=List[Ejercicio])
async def obtener_ejercicios(nivel: int):
    # Consultamos los ejercicios del nivel especificado
    consulta = ejercicios.select().where(
        ejercicios.c.nivel == nivel
    )

    ejercicios_registrados = await database.fetch_all(consulta)

    if not ejercicios_registrados:
        raise HTTPException(status_code=404, detail="No hay ejercicios para este nivel.")
    
    return ejercicios_registrados