from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from pkg.config.database import Base


class PrenotazioneDB(Base):
    __tablename__ = "prenotazioni"

    id = Column(Integer, primary_key=True, index=True)
    data_inizio = Column(DateTime, default=datetime.now)
    data_fine = Column(DateTime, nullable=True)
    attiva = Column(Boolean, default=True)
    libro_id = Column(Integer, ForeignKey("libri.id"))
    utente_id = Column(Integer, ForeignKey("utenti.id"))

    libro = relationship("LibroDB", back_populates="prenotazioni")
    utente = relationship("UtenteDB", back_populates="prenotazioni")