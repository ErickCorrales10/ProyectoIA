from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Operacion(BaseModel):
    a: float
    b:float

@app.post("/sumar")
def sumar(operacion: Operacion):
    return {"resultado": operacion.a + operacion.b}

@app.post("/restar")
def restar(operacion: Operacion):
    return {"resultado": operacion.a - operacion.b}

@app.post("/multiplicar")
def multiplicar(operacion: Operacion):
    return {"resultado": operacion.a * operacion.b}

@app.post("/dividir")
def dividir(operacion: Operacion):
    if operacion.b == 0:
        return {"error": "No se puede dividir por cero"}
    return {"resultado": operacion.a / operacion.b}