from modelos import ejercicios, preguntas_padres
from base_datos import database
from sqlalchemy import insert

# Ejercicios predefinidos por nivel y tipo
ejercicios_predefinidos = [
    # Nivel 1
    {"nombre": "Distinguir sonidos", "descripcion": "Escucha dos palabras y di cuál has escuchado.", "tipo": "Sonidos", "nivel": 1},
    {"nombre": "Secuencia de sonidos", "descripcion": "Escucha una secuencia de sonidos y repítela.", "tipo": "Memoria auditiva", "nivel": 1},
    {"nombre": "Completar sonidos", "descripcion": "Ayuda a completar las oraciones.", "tipo": "Memoria Vocabulario", "nivel": 1},

    # Nivel 2
    {"nombre": "Identificar sonidos iniciales", "descripcion": "Escucha palabras y di su sonido inicial.", "tipo": "Sonidos", "nivel": 2},
    {"nombre": "Sinónimos", "descripcion": "Encuentra sinónimos para cada palabra.", "tipo": "Vocabulario", "nivel": 2},
    {"nombre": "Adivinanzas", "descripcion": "Responde a las adivinanzas basadas en pistas.", "tipo": "Vocabulario", "nivel": 2},
    
    # Nivel 3
    {"nombre": "Sonidos cotidianos", "descripcion": "Escucha y reconoce sonidos cotidianos.", "tipo": "Sonidos", "nivel": 3},
    {"nombre": "Historias cortas", "descripcion": "Escucha historias y responde preguntas sobre ellas.", "tipo": "Memoria auditiva", "nivel": 3},
    {"nombre": "Secuencia de acciones", "descripcion": "Escucha y repite secuencias de acciones.", "tipo": "Memoria auditiva", "nivel": 3},
]

# Preguntas para padres
preguntas_padre = [
    {"pregunta": "¿Sabes qué es la afasia?", "nivel": 1},
    {"pregunta": "¿Sabes cómo ayudar a tu hijo con afasia?", "nivel": 1},
    {"pregunta": "¿Sabes qué es la disfasia?", "nivel": 2},
    {"pregunta": "¿Conoces los tipos de disfasia?", "nivel": 2},
    {"pregunta": "¿Sabes qué ejercicios ayudan con la afasia?", "nivel": 2},
    {"pregunta": "¿Has implementado juegos para mejorar la memoria auditiva?", "nivel": 3},
    {"pregunta": "¿Sabes cómo mejorar la comunicación con tu hijo?", "nivel": 3},
    {"pregunta": "¿Estás familiarizado con los recursos para el tratamiento de afasia?", "nivel": 3},
]

async def insertar_datos():
    ejercicios_existentes = await database.fetch_all("SELECT id FROM ejercicios")
    preguntas_existentes = await database.fetch_all("SELECT id FROM preguntas_padres")

    if ejercicios_existentes and preguntas_existentes:
        print("Los ejercicios y preguntas ya están insertados")
        return

    # Insertamos los ejercicios
    for ejercicio in ejercicios_predefinidos:
        consulta = insert(ejercicios).values(
            nombre=ejercicio["nombre"],
            descripcion=ejercicio["descripcion"],
            tipo=ejercicio["tipo"],
            nivel=ejercicio["nivel"]
        )

        await database.execute(consulta)

    # Insertamos las preguntas para los padres
    for preguntas in preguntas_padre:
        consulta = insert(preguntas_padres).values(
            pregunta=preguntas["pregunta"],
            nivel=preguntas["nivel"]
        )

        await database.execute(consulta)


