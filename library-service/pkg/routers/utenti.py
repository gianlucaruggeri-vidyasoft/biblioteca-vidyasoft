from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from pkg.config.database import get_db
from pkg.repositories.utenti import UtenteRepository
from pkg.schemas.utente import Utente, UtenteBase

router = APIRouter(prefix="/utenti", tags=["Utenti"])
utenti_repo = UtenteRepository()


@router.post("/", response_model=Utente)
def crea_utente(utente: UtenteBase, db: Session = Depends(get_db)):
    return utenti_repo.crea(db, utente)


@router.get("/", response_model=List[Utente])
def lista_utenti(db: Session = Depends(get_db)):
    return utenti_repo.leggi_tutti(db)
