from pydantic import BaseModel
from typing import List, Optional

class StartRequest(BaseModel):
    user_id: str

class RespuestaNivel(BaseModel):
    user_id: str
    nivel: str
    puntaje: str
    mensaje: str

class RegistrarProgreso(BaseModel):
    user_id: str
    nivel: int
    ejercicio: int
    completado: bool

class DetalleProgreso(BaseModel):
    nivel: int
    ejercicio: int
    completado: bool
    fecha: str

class ResumenProgreso(BaseModel):
    user_id: str
    progreso: List[DetalleProgreso]
    porcentaje_completado: float

class UsuarioNuevo(BaseModel):
    id: str
    nivel: int
    puntaje: int
    ejercicio_actual: int

class EjercicioBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo: str
    nivel: int

class Ejercicio(EjercicioBase):
    id: int

    class Config:
        orm_mode = True # Esto es necesario para convertir de SQLAlchemy a Pydantic

class Pregunta(BaseModel):
    pregunta: str
    nivel: int

    class Config:
        orm_mode = True