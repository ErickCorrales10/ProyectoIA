from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Modelo de datos
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




