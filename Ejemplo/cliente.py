""" import requests # Para enviar solicitudes a FastAPI desde el mismo archivo

def agregar_tarea():
    # Agregar tarea por teclado
    print('Crear nueva tarea')
    id = int(input('ID de la tarea: '))
    titulo = input('Título de la tarea: ')
    descripcion = input('Descripción de la tarea (opcional): ')
    
    nueva_tarea = {
        "id": id,
        "titulo": titulo,
        "descripcion": descripcion,
        "completado": False
    }

    respuesta =  requests.post("http://127.0.0.1:8000/tareas/", json=nueva_tarea)
    
    if respuesta.status_code == 200:
        print('Tarea agregada correctamente')
        print(respuesta.json())
    else:
        print("Error al agregar la tarea")
        print(respuesta.status_code, respuesta.text)

if __name__ == "__main__":
    agregar_tarea() """