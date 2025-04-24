from fastapi import APIRouter, HTTPException
from modelos import usuarios
from base_datos import database
from esquemas import StartRequest

router = APIRouter()

@router.post("/inicio")
async def iniciar_skill(req: StartRequest):
    usuario = await database.fetch_one(
                usuarios.select().
                where(usuarios.c.id == req.user_id))
    if usuario:
        return {"mensaje": "Sesión ya iniciada", "user_id": req.user_id}
    
    consulta = usuarios.insert().values(
        id = req.user_id,
        nivel = 1,
        puntaje = 0,
        ejercicio_actual = 1
    )

    await database.execute(consulta)
    return {"mensaje": "Juego iniciado", "user_id": req.user_id}