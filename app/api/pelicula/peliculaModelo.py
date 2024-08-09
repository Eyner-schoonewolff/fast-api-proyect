from pydantic import BaseModel
from typing import List


class PeliculaModelo(BaseModel):
    nombre: str
    descripcion: str
    generos: List[str]
    personajes: List[str]
