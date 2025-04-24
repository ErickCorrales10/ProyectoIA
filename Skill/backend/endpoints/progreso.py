from fastapi import APIRouter, HTTPException
from modelos import progreso, usuarios
from base_datos import database
from esquemas import RegistrarProgreso, ResumenProgreso, DetalleProgreso, UsuarioNuevo
from typing import List

router = APIRouter()

@router.post("/registrar-progreso")
async def registrar_progreso(datos: RegistrarProgreso):
    usuario = await database.fetch_one(
        usuarios.select().where(
            usuarios.c.id == datos.user_id
        )
    )

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    consulta = progreso.insert().values(
        user_id = datos.user_id,
        nivel = datos.nivel,
        ejercicio = datos.ejercicio,
        completado = datos.completado
    )

    await database.execute(consulta)
    return {"mensaje": "Progreso registrado correctamente"}

@router.get("/consulta-progreso", response_model=ResumenProgreso)
async def consulta_progreso(user_id: str):
    usuario = await database.fetch_one(usuarios.select().where(usuarios.c.id == user_id))

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    registros = await database.fetch_all(
        progreso.select().where(progreso.c.user_id == user_id)
    )

    if not registros:
        raise HTTPException(status_code=404, detail="No hay progreso registrado")
    
    detalles = [DetalleProgreso(
        nivel = r["nivel"],
        ejercicio = r["ejercicio"],
        completado = r["completado"],
        fecha = str(r["fecha"])
    ) for r in registros]

    total = len(detalles)
    completados = sum(1 for d in detalles if d.completado)
    porcentaje = (completados / total) * 100 if total > 0 else 0

    return ResumenProgreso(
        user_id = user_id,
        progreso = detalles,
        porcentaje_completado = porcentaje
    )

# Endpoint para consultar los usuarios registrados en la base de datos
@router.get("/consultar-usuarios", response_model=List[UsuarioNuevo])
async def obtener_usuarios():
    consulta = usuarios.select()
    resultados = await database.fetch_all(consulta)
    return resultados