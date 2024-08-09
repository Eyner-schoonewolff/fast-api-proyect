from fastapi import APIRouter
from typing import List
from app.api.pelicula.peliculaModelo import PeliculaModelo

pelicula = APIRouter()

@pelicula.get("/", response_model=List[PeliculaModelo])
async def index():
    return []