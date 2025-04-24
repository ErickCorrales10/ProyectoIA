from fastapi import APIRouter
from modelos import usuarios
from base_datos import database
from esquemas import UsuarioNuevo

router = APIRouter()

@router.post("/agregar-usuario")
async def agregar_usuario(datos: UsuarioNuevo):
    consulta = usuarios.insert().values(
        id = datos.id,
        nivel = datos.nivel,
        puntaje = datos.puntaje,
        ejercicio_actual = datos.ejercicio_actual
    )

    await database.execute(consulta)
    return {"mensaje": "Usuario agregado correctamente", "usuario": datos}