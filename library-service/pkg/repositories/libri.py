from sqlalchemy.orm import Session

from pkg.models.libro import LibroDB
from pkg.schemas.libro import LibroBase


class LibroRepository:
    def crea(self, db: Session, libro: LibroBase):
        db_libro = LibroDB(**libro.model_dump())
        db.add(db_libro)
        db.commit()
        db.refresh(db_libro)
        return db_libro

    def leggi_tutti(self, db: Session):
        return db.query(LibroDB).all()

    def leggi_uno(self, db: Session, id: int):
        return db.query(LibroDB).filter(LibroDB.id == id).first()

    def aggiorna(self, db: Session, id: int, dati: LibroBase):
        obj = db.query(LibroDB).filter(LibroDB.id == id).first()
        if obj:
            obj.titolo = dati.titolo
            obj.autore = dati.autore
            obj.copie_totali = dati.copie_totali
            db.commit()
            db.refresh(obj)
            return obj
        return None

    def elimina(self, db: Session, id: int):
        obj = db.query(LibroDB).filter(LibroDB.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False
