from sqlalchemy import Column, Integer, String, Table, ARRAY
from database.db import metadata

peliculas = Table(
    "peliculas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(50)),
    Column("descripcion", String(250)),
    Column("generos", ARRAY(String)),
    Column("personajes", ARRAY(String)),
)
