import json
import boto3
import botocore
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from pkg.config.database import get_db, AWS_PARAMS, TOPIC_ARN
from pkg.repositories.libri import LibroRepository
from pkg.repositories.prenotazioni import PrenotazioneRepository
from pkg.repositories.utenti import UtenteRepository
from pkg.schemas.prenotazione import Prenotazione, PrenotazioneCreate, PrenotazioneUpdate
from pkg.services.reservations import PrenotazioneService

router = APIRouter(prefix="/prenotazioni", tags=["Prenotazioni"])

# Inizializzazione client SNS per le notifiche
sns_client = boto3.client("sns", **AWS_PARAMS)

# Inizializzazione repository e servizi
libri_repo = LibroRepository()
utenti_repo = UtenteRepository()
prenotazioni_repo = PrenotazioneRepository()
prenotazione_service = PrenotazioneService(libri_repo, utenti_repo, prenotazioni_repo)

@router.post("/", response_model=Prenotazione)
def crea_prenotazione(pren: PrenotazioneCreate, db: Session = Depends(get_db)):
    try:
        # 1. Salva la prenotazione su Postgres
        nuova_prenotazione = prenotazione_service.crea(db, pren)
        
        print(f"\n🚀 [DEBUG] Prenotazione salvata su DB (ID: {nuova_prenotazione.id})")
        print(f"📍 [DEBUG] Invio notifica a Topic: {TOPIC_ARN}")

        # 2. Prepara il payload per il Worker (MongoDB + Email)
        payload_email = {
            "to_email": nuova_prenotazione.utente.email,
            "subject": "Conferma Prenotazione Libro",
            "body": f"Ciao {nuova_prenotazione.utente.nome}, hai prenotato con successo '{nuova_prenotazione.libro.titolo}'!"
        }

        # 3. Prova a pubblicare su SNS
        try:
            response = sns_client.publish(
                TopicArn=TOPIC_ARN,
                Message=json.dumps(payload_email)
            )
            print(f"✅ [DEBUG] Notifica SNS inviata con successo! ID: {response.get('MessageId')}")
        except botocore.exceptions.ClientError as e:
            print(f"❌ [DEBUG ERROR] AWS SNS ha risposto con errore: {e.response['Error']['Message']}")
        except Exception as e:
            print(f"⚠️ [DEBUG ERROR] Errore generico invio SNS: {str(e)}")

        return nuova_prenotazione

    except ValueError as exc:
        print(f"🛑 [DEBUG] Errore validazione: {str(exc)}")
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as e:
        print(f"🔥 [DEBUG] Errore imprevisto nella POST: {str(e)}")
        raise HTTPException(status_code=500, detail="Errore interno del server")

@router.put("/{prenotazione_id}/termina", response_model=Prenotazione)
def termina_prenotazione(prenotazione_id: int, db: Session = Depends(get_db)):
    print(f"🛠️ [DEBUG] Termino prenotazione ID: {prenotazione_id}")
    try:
        result = prenotazione_service.termina(db, prenotazione_id)
        if not result:
            raise HTTPException(status_code=404, detail="Prenotazione non trovata")
        return result
    except Exception as e:
        print(f"🔥 [DEBUG] Errore nella PUT: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{prenotazione_id}", response_model=Prenotazione)
def aggiorna_prenotazione(
    prenotazione_id: int,
    payload: PrenotazioneUpdate,
    db: Session = Depends(get_db),
):
    print(f"📝 [DEBUG] Aggiorno prenotazione ID: {prenotazione_id}")
    try:
        result = prenotazione_service.aggiorna(db, prenotazione_id, payload)
        if not result:
            raise HTTPException(status_code=404, detail="Prenotazione non trovata")
        return result
    except Exception as e:
        print(f"🔥 [DEBUG] Errore nella PATCH: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))