from fastapi.responses import JSONResponse
import random


# Lista de pares de palabras a escuchar
pares_palabras = [
    (1, 'gato', 'pato'),
    (2, 'manzana', 'banana'),
    (3, "coche", "choque"),
    (4, "silla", "villa"),
    (5, "perro", "cerro"),
    (6, 'fruta', 'ruta'),
    (7, 'avión', 'camión'),
    (8, 'sol', 'rol')
]

palabras = random.choice(pares_palabras)
""" print(type(pares_palabras))
print(pares_palabras[0])
print(palabras)
palabra_1, palabra_2 = palabras
print(palabra_1) """

# Seleccionamos las palabras a escuchar
par_correcto = random.choice(pares_palabras)

# Función para manejar el juego
async def handle_adivina_palabra():
    return JSONResponse(content={
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Escucha con atención: gato...pato. ¿Cuál palabra escuchaste?"
            },
            "shouldEndSession": False
        }
    })

# Función para escuchar las instrucciones del juego
async def adivina_palabras_instrucciones():
    return JSONResponse(content={
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Debes escuchar una oración y decir cuál de dos palabras escuchaste. ¿Listo para empezar?"
                    },
                    "shouldEndSession": False
                }
            })