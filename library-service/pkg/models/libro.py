from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship

from pkg.config.database import Base


class LibroDB(Base):
    __tablename__ = "libri"

    id = Column(Integer, primary_key=True, index=True)
    titolo = Column(String, index=True)
    autore = Column(String)
    copie_totali = Column(Integer, default=1)
    citazioni = Column(JSON, default=[])

    prenotazioni = relationship("PrenotazioneDB", back_populates="libro")