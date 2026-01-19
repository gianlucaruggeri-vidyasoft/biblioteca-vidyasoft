from pydantic import BaseModel


class LibroBase(BaseModel):
    titolo: str
    autore: str
    copie_totali: int


class Libro(LibroBase):
    id: int

    class Config:
        orm_mode = True

