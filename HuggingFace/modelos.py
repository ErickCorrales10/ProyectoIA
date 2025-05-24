from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from base_datos import metadata
from datetime import datetime, timezone

chat_preguntas = Table(
    "chat_preguntas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("pregunta", Text, nullable=False),
    Column("respuesta", Text, nullable=False),
    Column("fecha_creacion", DateTime, default=datetime.now(timezone.utc)),
)