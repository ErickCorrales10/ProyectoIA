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

# Seleccionar la oración dependiendo de las palabras
def seleccionar_oracion(indice, palabra_escogida):
    match indice:
        case 1:
            return "El gato saltó por la ventana para tomar el sol." if palabra_escogida == 'gato' else "En el lago el pato paseaba por el agua."
            
        case 2:
            if palabra_escogida == 'manzana':
                return "La manzana cayó del árbol y rodó por el césped."
            else:
                return "El mono peló una banana y se la comió felizmente."
            
        case 3:
            return "El coche rojo aceleró por la autopista sin detenerse." if palabra_escogida == "coche" else "Hubo un pequeño choque en la esquina, pero nadie salió herido."
            
        case 4:
            if palabra_escogida == 'silla':
                return "Juan se sentó en la silla y comenzó a leer su libro."
            else:
                return "Pasaron el verano en una villa junto al mar."
        
        case 5:
            if palabra_escogida == 'perro':
                return "El perro ladró fuerte cuando vio al cartero acercarse."
            else:
                return "Subimos al cerro para ver el atardecer desde la cima."
        
        case 6:
            if palabra_escogida == 'fruta':
                return "Cada mañana desayuno con una fruta diferente."
            else:
                return "Tomamos la ruta más larga para disfrutar del paisaje."
        
        case 7:
            if palabra_escogida == 'avión':
                return "El avión despegó con destino a París al amanecer."
            else:
                return "Un camión de carga pasó frente a la tienda haciendo mucho ruido."
            
        case 8:
            if palabra_escogida == 'sol':
                return "El gato dormía plácidamente bajo el sol del mediodía."
            else:
                return "Cada actor interpretó su rol con gran emoción en la obre de teatro."

# Función para manejar el juego
async def handle_escucha_palabra():
    # Seleccionamos el par de palabras a escuchar
    palabras = random.choice(pares_palabras)
    indice, palabra_1, palabra_2 = palabras
    palabras_escogidas = (palabra_1, palabra_2)
    palabra_escogida = random.choice(palabras_escogidas)
    print(palabras_escogidas)
    print(palabra_escogida)

    # Guardamos la oración seleccionada
    oracion = seleccionar_oracion(indice, palabra_escogida)
    pregunta = f"¿Qué palabra escuchaste?...¿{palabras_escogidas[0]}...o {palabras_escogidas[1]}?"

    texto_a_decir = f"{oracion} {pregunta}"

    return JSONResponse(content={
        "version": "1.0",
        "sessionAttributes": {
            "palabra_correcta": palabra_escogida
        },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": texto_a_decir
            },
            "shouldEndSession": False
        }
    })

# Función para escuchar las instrucciones del juego
async def escucha_palabras_instrucciones():
    return JSONResponse(content={
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Debes escuchar una oración y decir cuál de dos palabras escuchaste."
                    },
                    "shouldEndSession": False
                }
            })

# Función para verificar si la palabra dicha es la correcta
async def verificar_palabra(valor_usuario: str, palabra_correcta: str):
    if valor_usuario == palabra_correcta:
        mensaje = f"Correcto!!! Has escuchado bien!!!."
    else:
        mensaje = f"No es correcto. Intenta de nuevo."

    return JSONResponse(content={
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": mensaje
            },
            "shouldEndSession": False
        }
    })