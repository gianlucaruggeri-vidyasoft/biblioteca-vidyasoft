from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from pkg.config.database import Base


class UtenteDB(Base):
    __tablename__ = "utenti"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    prenotazioni = relationship("PrenotazioneDB", back_populates="utente")

