# init_db.py

from base_datos import engine, metadata
from modelos import chat_preguntas  # importa los modelos para que estén registrados en metadata

# Crea las tablas
metadata.create_all(engine)
print("Tablas creadas correctamente.")
