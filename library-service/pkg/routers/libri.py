from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from pkg.config.database import get_db
from pkg.repositories.libri import LibroRepository
from pkg.schemas.libro import Libro, LibroBase

router = APIRouter(prefix="/libri", tags=["Libri"])
libri_repo = LibroRepository()


@router.post("/", response_model=Libro)
def crea_libro(libro: LibroBase, db: Session = Depends(get_db)):
    return libri_repo.crea(db, libro)


@router.get("/", response_model=List[Libro])
def lista_libri(db: Session = Depends(get_db)):
    return libri_repo.leggi_tutti(db)
