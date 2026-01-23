from sqlalchemy.orm import Session
from pkg.models.libro import LibroDB
from pkg.schemas.libro import LibroCreate, LibroUpdate

class LibroRepository:
    def crea(self, db: Session, libro: LibroCreate):
        # model_dump() estrae automaticamente tutti i campi, inclusi autore e citazioni
        db_libro = LibroDB(**libro.model_dump())
        db.add(db_libro)
        db.commit()
        db.refresh(db_libro)
        return db_libro

    def leggi_tutti(self, db: Session):
        return db.query(LibroDB).all()

    def leggi_uno(self, db: Session, id: int):
        return db.query(LibroDB).filter(LibroDB.id == id).first()

    def aggiorna(self, db: Session, id: int, dati: LibroUpdate):
        obj = db.query(LibroDB).filter(LibroDB.id == id).first()
        if obj:
            # exclude_unset=True ignora i campi non inviati (None)
            for key, value in dati.model_dump(exclude_unset=True).items():
                setattr(obj, key, value)
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