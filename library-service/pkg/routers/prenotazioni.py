import json
import boto3
import botocore
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from pkg.config.database import get_db, AWS_PARAMS, TOPIC_ARN
from pkg.repositories.prenotazioni import PrenotazioneRepository
from pkg.repositories.libri import LibroRepository
from pkg.repositories.utenti import UtenteRepository
from pkg.schemas.prenotazione import Prenotazione, PrenotazioneCreate, PrenotazioneUpdate

router = APIRouter(prefix="/api/internal/prenotazioni", tags=["Prenotazioni"])

sns_client = boto3.client("sns", **AWS_PARAMS)

prenotazioni_repo = PrenotazioneRepository()
libri_repo = LibroRepository()
utenti_repo = UtenteRepository()

@router.get("/v1", response_model=List[Prenotazione])
def lista_prenotazioni(db: Session = Depends(get_db)):
    return prenotazioni_repo.leggi_tutti(db)

@router.get("/{id}/v1", response_model=Prenotazione)
def leggi_prenotazione(id: int, db: Session = Depends(get_db)):
    pren = prenotazioni_repo.leggi_uno(db, id)
    if not pren:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    return pren

@router.post("/v1", response_model=Prenotazione)
def crea_prenotazione(dati: PrenotazioneCreate, db: Session = Depends(get_db)):
    libro = libri_repo.leggi_uno(db, dati.libro_id)
    utente = utenti_repo.leggi_uno(db, dati.utente_id)

    if not libro:
        raise HTTPException(status_code=404, detail=f"Libro {dati.libro_id} non trovato")
    if not utente:
        raise HTTPException(status_code=404, detail=f"Utente {dati.utente_id} non trovato")

    try:
        nuova_prenotazione = prenotazioni_repo.crea(db, dati)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore DB: {str(e)}")

    try:
        payload_email = {
            "email_type": "RESERVE",
            "reservationId": nuova_prenotazione.id,
            "to_email": utente.email,
            "subject": "Conferma Prenotazione",
            "body": f"Ciao {utente.nome}, hai prenotato '{libro.titolo}'.",
            "autore": libro.autore,
            "citazioni": libro.citazioni
        }

        sns_client.publish(
            TopicArn=TOPIC_ARN,
            Message=json.dumps(payload_email)
        )

    except botocore.exceptions.ClientError:
        pass
    except Exception:
        pass

    return nuova_prenotazione

@router.put("/{id}/v1", response_model=Prenotazione)
def aggiorna_totale_prenotazione(id: int, dati: PrenotazioneUpdate, db: Session = Depends(get_db)):
    pren = prenotazioni_repo.aggiorna(db, id, dati)
    if not pren:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    return pren

@router.patch("/{id}/v1", response_model=Prenotazione)
def aggiorna_parziale_prenotazione(id: int, dati: PrenotazioneUpdate, db: Session = Depends(get_db)):
    if dati.attiva is False:
        pren = prenotazioni_repo.termina(db, id)
        if not pren:
             raise HTTPException(status_code=400, detail="Prenotazione non trovata o già terminata")
        return pren

    pren = prenotazioni_repo.aggiorna(db, id, dati)
    if not pren:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    return pren