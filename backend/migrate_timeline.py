
import uuid
from database import SessionLocal, engine
import models
import models_v2 as m2
from datetime import datetime
import json

def migrate():
    db = SessionLocal()
    try:
        # 1. Crear la taula i el tipus ENUM si no existeixen
        # Nota: Base.metadata.create_all és segur i no esborra dades
        m2.Base.metadata.create_all(bind=engine)
        print("Taules creades/verificades.")

        # 2. Migració de dades
        # A) Notes dels Deals (V1)
        deals = db.query(models.Deal).filter(models.Deal.notes_humanes != None, models.Deal.notes_humanes != '').all()
        for d in deals:
            act = m2.ActivitatsMunicipi(
                municipi_id=d.municipi_id,
                deal_id=d.id,
                tipus_activitat=m2.TipusActivitat.nota_manual,
                data_activitat=d.updated_at or d.created_at or datetime.now(),
                notes_comercial=d.notes_humanes,
                contingut={"origen": "notes_deal_v1"}
            )
            db.add(act)
        print(f"Migrades {len(deals)} notes de deals.")

        # B) Trucades (V2)
        trucades = db.query(m2.TrucadaV2).all()
        for t in trucades:
            act = m2.ActivitatsMunicipi(
                municipi_id=t.municipi_id,
                tipus_activitat=m2.TipusActivitat.trucada,
                data_activitat=t.data,
                contingut={
                    "durada_minuts": t.durada_minuts,
                    "qui_va_contestar": t.qui_va_contestar.value if t.qui_va_contestar else None,
                    "resum_ia": t.resum_ia
                },
                notes_comercial=t.notes_breus
            )
            db.add(act)
        print(f"Migrades {len(trucades)} trucades.")

        # C) Reunions (V2)
        reunions = db.query(m2.ReunioV2).all()
        for r in reunions:
            act = m2.ActivitatsMunicipi(
                municipi_id=r.municipi_id,
                tipus_activitat=m2.TipusActivitat.reunio,
                data_activitat=r.data,
                contingut={
                    "tipus_reunio": r.tipus,
                    "assistents": r.assistents,
                    "aar_completat": r.aar_completat,
                    "poi_mes_reaccio": r.poi_mes_reaccio,
                    "objeccio": r.objeccio_principal
                },
                notes_comercial=r.notes_aar
            )
            db.add(act)
        print(f"Migrades {len(reunions)} reunions.")

        # D) Emails (V2)
        emails = db.query(m2.EmailV2).all()
        for e in emails:
            act = m2.ActivitatsMunicipi(
                municipi_id=e.municipi_id,
                tipus_activitat=m2.TipusActivitat.email_enviat, # Simplificat per ara o segons direccio
                data_activitat=e.data_enviament,
                contingut={
                    "assumpte": e.assumpte,
                    "obert": e.obert,
                    "sentiment": e.sentiment_resposta.value if e.sentiment_resposta else None
                },
                notes_comercial=e.cos[:500] if e.cos else ""
            )
            db.add(act)
        print(f"Migrats {len(emails)} emails.")

        db.commit()
        print("Migració completada amb èxit.")

    except Exception as e:
        db.rollback()
        print(f"Error durant la migració: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
