from typing import List, Optional
from pydantic import BaseModel

class LibroBase(BaseModel):
    titolo: str
    autore: str
    copie_totali: int = 1
    citazioni: List[str] = []

class LibroCreate(LibroBase):
    pass

class Libro(LibroBase):
    id: int

    class Config:
        orm_mode = True

class LibroUpdate(BaseModel):
    titolo: Optional[str] = None
    autore: Optional[str] = None
    copie_totali: Optional[int] = None
    citazioni: Optional[List[str]] = None