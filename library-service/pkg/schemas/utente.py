from typing import Optional
from pydantic import BaseModel

class UtenteBase(BaseModel):
    nome: str
    email: str

class UtenteCreate(UtenteBase):
    pass

class Utente(UtenteBase):
    id: int

    class Config:
        orm_mode = True

class UtenteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None