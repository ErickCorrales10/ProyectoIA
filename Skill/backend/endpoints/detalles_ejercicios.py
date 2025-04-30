from modelos import ejercicios, ejercicios_detalle
from base_datos import database
from sqlalchemy import select, insert, func
import json

async def insertar_detalles():
    consulta = select(ejercicios.c.id).where(
        ejercicios.c.nombre == "Distinguir sonidos"
    )

    resultado = await database.fetch_one(consulta)

    if not resultado:
        print("Ejercicios 'Distinguir sonidos' no encontrado")
        return
    
    ejercicio_id = resultado[0]

    # Verificar si los ejercicios ya están insertados
    verificar_ejercicios = select(func.count()).select_from(ejercicios_detalle).where(
        ejercicios_detalle.c.ejercicio_id == ejercicio_id
    )
    verificar = await database.fetch_val(verificar_ejercicios)

    if verificar > 0: 
        print('Ya existen detalles para los ejercicios')

    # Detalle para este ejercicio
    detalles = [
        {
            "instrucciones": "¿Cuál palabra escuchaste?",
            "opciones": json.dumps(["casa", "caza"]),
            "respuesta_correcta": "casa"
        },
        {
            "instrucciones": "¿Qué palabra oíste?",
            "opciones": json.dumps(["pala", "bala"]),
            "respuesta_correcta": "bala"
        }
    ]

    # Insertar en la tabla ejercicios_detalle
    for detalle in detalles:
        consulta = insert(ejercicios_detalle).values(
            ejercicio_id=ejercicio_id,
            instruccion=detalle["instrucciones"],
            opciones=detalle["opciones"],
            respuesta_correcta=detalle["respuesta_correcta"]
        )

    print('Detalles del ejercicio Distinguir sonidos insertados correctamente')