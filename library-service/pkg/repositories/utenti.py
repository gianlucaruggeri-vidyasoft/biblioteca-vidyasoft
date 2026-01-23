from sqlalchemy.orm import Session
from pkg.models.utente import UtenteDB
from pkg.schemas.utente import UtenteCreate, UtenteUpdate

class UtenteRepository:
    def crea(self, db: Session, utente: UtenteCreate):
        db_utente = UtenteDB(**utente.model_dump())
        db.add(db_utente)
        db.commit()
        db.refresh(db_utente)
        return db_utente

    def leggi_tutti(self, db: Session):
        return db.query(UtenteDB).all()

    def leggi_uno(self, db: Session, id: int):
        return db.query(UtenteDB).filter(UtenteDB.id == id).first()

    def aggiorna(self, db: Session, id: int, dati: UtenteUpdate):
        obj = db.query(UtenteDB).filter(UtenteDB.id == id).first()
        if obj:
            for key, value in dati.model_dump(exclude_unset=True).items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
            return obj
        return None

    def elimina(self, db: Session, id: int):
        obj = db.query(UtenteDB).filter(UtenteDB.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False