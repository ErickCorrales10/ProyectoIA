from fastapi import APIRouter, HTTPException
from modelos import usuarios
from base_datos import database
from esquemas import RespuestaNivel

router = APIRouter()

@router.post("/avanzar", response_model=RespuestaNivel)
async def avanzar_nivel(user_id: str):
    usuario = await database.fetch_one(
        usuarios.select().
        where(
            usuarios.c.id == user_id
        )
    )

    if not usuario:
        # return {"mensaje": "Usuario no encontrado"}
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    nivel_actual = usuario["nivel"]
    puntaje = usuario["puntaje"]

    if nivel_actual >= 3:
        return RespuestaNivel(
            user_id=user_id,
            nivel=nivel_actual,
            puntaje=puntaje,
            mensaje="Ya estás en el nivel máximo"
        )
    
    if puntaje >= 100:
        nuevo_nivel = nivel_actual + 1
        await database.execute(
            usuarios.update().
                where(usuarios.c.id == user_id).
                values(nivel = nuevo_nivel)
            )
        mensaje = "Has subido al siguiente nivel"
    else:
        nuevo_nivel = nivel_actual
        mensaje = "Aún no tienes suficiente puntaje para avanzar"

    return RespuestaNivel(
        user_id=user_id,
        nivel=nuevo_nivel,
        puntaje=puntaje,
        mensaje=mensaje
    )