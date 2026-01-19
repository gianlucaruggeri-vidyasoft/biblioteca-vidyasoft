from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PrenotazioneCreate(BaseModel):
    libro_id: int
    utente_id: int


class Prenotazione(BaseModel):
    id: int
    data_inizio: datetime
    data_fine: Optional[datetime]
    attiva: bool
    libro_id: int
    utente_id: int

    class Config:
        orm_mode = True


class PrenotazioneUpdate(BaseModel):
    data_fine: Optional[datetime] = None
    attiva: Optional[bool] = None

