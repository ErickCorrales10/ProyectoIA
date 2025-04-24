from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from base_datos import metadata
from datetime import datetime, timezone

usuarios = Table(
    "usuarios",
    metadata,
    Column("id", String, primary_key=True),
    Column("nivel", Integer, default=1),
    Column("puntaje", Integer, default=0),
    Column("ejercicio_actual", Integer, default=1)
)

# Tabla para el progreso del usuario
progreso = Table(
    "progreso",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", String, index=True),
    Column("nivel", Integer),
    Column("ejercicio", Integer),
    Column("completado", Boolean, default=False),
    Column("fecha", DateTime, default=lambda: datetime.now(timezone.utc))
)

# Tabla para los ejercicios
ejercicios = Table(
    "ejercicios",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", String, nullable=False),
    Column("descripcion", String),
    Column("tipo", String),
    Column("nivel", Integer)
)

# Tabla para las preguntas a los padres
preguntas_padres = Table(
    "preguntas_padres",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pregunta", String),
    Column("nivel", Integer)
)
