from base_datos import engine
from modelos import metadata

metadata.create_all(engine)
print("Tablas creadas correctamente")