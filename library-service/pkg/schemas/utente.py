from pydantic import BaseModel


class UtenteBase(BaseModel):
    nome: str
    email: str


class Utente(UtenteBase):
    id: int

    class Config:
        orm_mode = True

