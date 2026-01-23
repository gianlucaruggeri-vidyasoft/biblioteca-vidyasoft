from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from pkg.config.database import get_db
from pkg.repositories.libri import LibroRepository
from pkg.schemas.libro import Libro, LibroCreate, LibroUpdate

router = APIRouter(prefix="/api/internal/libri", tags=["Libri"])
repo = LibroRepository()

@router.get("/v1", response_model=List[Libro])
def lista_libri(db: Session = Depends(get_db)):
    return repo.leggi_tutti(db)

@router.get("/{id}/v1", response_model=Libro)
def leggi_libro(id: int, db: Session = Depends(get_db)):
    db_libro = repo.leggi_uno(db, id)
    if db_libro is None:
        raise HTTPException(status_code=404, detail="Libro non trovato")
    return db_libro

@router.post("/v1", response_model=Libro)
def crea_libro(libro: LibroCreate, db: Session = Depends(get_db)):
    return repo.crea(db, libro)

