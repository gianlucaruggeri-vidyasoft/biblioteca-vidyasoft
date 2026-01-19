from sqlalchemy.orm import Session

from pkg.repositories.libri import LibroRepository
from pkg.repositories.prenotazioni import PrenotazioneRepository
from pkg.repositories.utenti import UtenteRepository
from pkg.schemas.prenotazione import PrenotazioneCreate, PrenotazioneUpdate


class PrenotazioneService:
  

    def __init__(
        self,
        libro_repo: LibroRepository,
        utente_repo: UtenteRepository,
        prenotazione_repo: PrenotazioneRepository,
    ):
        self.libri = libro_repo
        self.utenti = utente_repo
        self.prenotazioni = prenotazione_repo

    def crea(self, db: Session, payload: PrenotazioneCreate):
        if not self.libri.leggi_uno(db, payload.libro_id):
            raise ValueError("Libro non trovato")
        if not self.utenti.leggi_uno(db, payload.utente_id):
            raise ValueError("Utente non trovato")
        return self.prenotazioni.crea(db, payload)

    def termina(self, db: Session, prenotazione_id: int):
        return self.prenotazioni.termina(db, prenotazione_id)

    def aggiorna(self, db: Session, prenotazione_id: int, payload: PrenotazioneUpdate):
        return self.prenotazioni.aggiorna(db, prenotazione_id, payload)
