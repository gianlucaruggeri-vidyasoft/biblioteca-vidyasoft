from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from pkg.config.database import get_db
from pkg.repositories.utenti import UtenteRepository
from pkg.schemas.utente import Utente, UtenteCreate, UtenteUpdate

router = APIRouter(prefix="/api/internal/utenti", tags=["Utenti"])
repo = UtenteRepository()

@router.get("/v1", response_model=List[Utente])
def lista_utenti(db: Session = Depends(get_db)):
    return repo.leggi_tutti(db)

@router.get("/{id}/v1", response_model=Utente)
def leggi_utente(id: int, db: Session = Depends(get_db)):
    db_utente = repo.leggi_uno(db, id)
    if db_utente is None:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return db_utente

@router.post("/v1", response_model=Utente)
def crea_utente(utente: UtenteCreate, db: Session = Depends(get_db)):
    return repo.crea(db, utente)

