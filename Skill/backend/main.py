from fastapi import FastAPI
from base_datos import database, engine
from modelos import metadata
from contextlib import asynccontextmanager
from endpoints.insertar_ejercicios import insertar_datos
from endpoints.detalles_ejercicios import insertar_detalles

metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Conectando a la base de datos....")
    await database.connect()
    print('Conectado a la base de datos')

    # Insertar ejercicios
    await insertar_datos()
    await insertar_detalles()

    yield
    print("Desconectado de la base de datos...")
    await database.disconnect()

app = FastAPI(
    title = "Skill Afasia/Disfasia",
    lifespan=lifespan)


# Registro de endpoints
from endpoints.inicio import router as inicio_router
from endpoints.niveles import router as niveles_router
from endpoints.progreso import router as progreso_router
from endpoints.usuarios import router as usuarios_router
from endpoints.ejercicios import router as ejercicios_router
from endpoints.preguntas_padres import router as preguntas_padres_router
from endpoints.alexa import router as alexa_router

app.include_router(inicio_router, prefix="/api", tags=["Inicio"])
app.include_router(niveles_router, prefix="/api", tags=["Niveles"])
app.include_router(progreso_router, prefix="/api", tags=["Progreso"])
app.include_router(usuarios_router, prefix="/api", tags=["Usuarios"])
app.include_router(ejercicios_router, prefix="/api", tags=["Ejercicios"])
app.include_router(preguntas_padres_router, prefix="/api", tags=["Preguntas padres"])
app.include_router(alexa_router, prefix="/api", tags=["Alexa"])
