from fastapi.responses import JSONResponse
import random

palabras_iniciales = [
    (1, "sol", "soltar", "subida", "salida"),
    (2, "casa", "calor", "cloro", "cuarto"),
    (3, "ratón", "rato", "riqueza", "rubí"),
    (4, "mesa", "meseta", "mariposa", "mono"),
    (5, "libro", "libreta", "lápiz", "lúcido"),
    (6, "perro", "persona", "poste", "podrido"),
    (7, "flor", "florería", "filoso", "flácido"),
    (8, "gato", "garganta", "guante", "guía"),
    (9, "barco", "bazuca", "bueno", "bonito"),
    (10, "zapato", "zarpar", "zorro", "zona"),
    (11, "tenis", "tenaza", "tulipán", "tostada"),
    (12, "nube", "nuevo", "novedad", "noticia"),
    (13, "vaca", "vaso", "viento", "ventana"),
    (14, "diente", "dieta", "doctor", "dominio"),
    (15, "juguete", "jugar", "jaqueca", "joroba"),
    (16, "rana", "rata", "roer", "ronda"),
    (17, "cama", "calle", "color", "claxón"),
    (18, "estrella", "estres", "exceder", "extensión"),
    (19, "hoja", "hora", "higo", "hijo"),
    (20, "pantalla", "pantalón", "pintura", "persiana")
]

def seleccionar_palabras():
    tupla = random.choice(palabras_iniciales)
    indice, palabra_seleccionada, palabra_correcta, palabra_incorrecta1, palabra_incorrecta2 = tupla
    print(tupla)
    
    return palabra_seleccionada, palabra_correcta, palabra_incorrecta1, palabra_incorrecta2

async def handle_sonidos_iniciales():
    palabra_seleccionada, palabra_correcta, palabra_incorrecta1, palabra_incorrecta2 = seleccionar_palabras()
    palabras_elegir = [palabra_correcta, palabra_incorrecta1, palabra_incorrecta2]

    """ print(f"La palabra seleccionada es: {palabra_seleccionada}\n" +
        f"La palabra correcta a comparar es: {palabra_correcta}\n" +
        f"Las palabras incorrectas son: {palabra_incorrecta1, palabra_incorrecta2}\n") """

    texto_a_decir = f"¿Qué palabra empieza por el mismo sonido que {palabra_seleccionada}..."
    texto_a_decir += f"{palabras_elegir.pop(random.randrange(len(palabras_elegir)))}, "
    texto_a_decir += f"{palabras_elegir.pop(random.randrange(len(palabras_elegir)))}, "
    texto_a_decir += f"{palabras_elegir[0]}?"

    return JSONResponse(content={
        "version": "1.0",
        "sessionAttributes": {
            "palabra_correcta": palabra_correcta
        },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": texto_a_decir
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