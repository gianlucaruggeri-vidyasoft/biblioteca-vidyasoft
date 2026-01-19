from datetime import datetime

from sqlalchemy.orm import Session

from pkg.models.prenotazione import PrenotazioneDB
from pkg.schemas.prenotazione import PrenotazioneCreate, PrenotazioneUpdate


class PrenotazioneRepository:
    def crea(self, db: Session, dati: PrenotazioneCreate):
        nuova = PrenotazioneDB(libro_id=dati.libro_id, utente_id=dati.utente_id)
        db.add(nuova)
        db.commit()
        db.refresh(nuova)
        return nuova

    def leggi_tutti(self, db: Session):
        return db.query(PrenotazioneDB).all()

    def leggi_uno(self, db: Session, id: int):
        return db.query(PrenotazioneDB).filter(PrenotazioneDB.id == id).first()

    def termina(self, db: Session, id: int):
        prenotazione = self.leggi_uno(db, id)
        if prenotazione and prenotazione.attiva:
            prenotazione.attiva = False
            prenotazione.data_fine = datetime.now()
            db.commit()
            db.refresh(prenotazione)
            return prenotazione
        return None

    def aggiorna(self, db: Session, id: int, dati: PrenotazioneUpdate):
        prenotazione = self.leggi_uno(db, id)
        if not prenotazione:
            return None

        for key, value in dati.model_dump(exclude_unset=True).items():
            setattr(prenotazione, key, value)

        db.commit()
        db.refresh(prenotazione)
        return prenotazione
