import requests # Para enviar solicituders a FastAPI desde el mismo archivo

def agregar_tarea():
    nueva_tarea = {
        "id": 1,
        "titulo": "Tarea de ejemplo",
        "descripcion": "Descripción de la tarea",
        "completado": False
    }

    respuesta =  requests.post("http://127.0.0.1:8000/tareas/", json=nueva_tarea)
    print(respuesta.json())

if __name__ == "__main__":
    agregar_tarea()