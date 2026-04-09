import os
import sys
import logging
import argparse
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

# Afegir el directori pare al path per trobar models i database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine
import models  # V1
import models_v2  # V2

# Configuració de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("migration_v1_v2.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def migrate(dry_run=True):
    db: Session = SessionLocal()
    if dry_run:
        logger.info("=== MODE DRY-RUN ACTIVAT (No es guardaran canvis) ===")
    
    try:
        # 1. MAPPING DICTS
        municipi_mapping = {}  # V1_id -> V2_id
        contacte_mapping = {}  # V1_id -> V2_id
        processed_v2_municipis = set() # Track for MemoriaMunicipi
        
        # 2. MIGRACIÓ MUNICIPIS
        logger.info("Iniciant migració de Municipis...")
        v1_municipis = db.query(models.Municipi).all()
        logger.info(f"Trobats {len(v1_municipis)} municipis a V1.")
        
        for v1_m in v1_municipis:
            # Crear V2 MunicipiLifecycle
            # Verifiquem si ja existeix pel nom per evitar duplicats en cas de re-migració parcial
            v2_m = db.query(models_v2.MunicipiLifecycle).filter(models_v2.MunicipiLifecycle.nom == v1_m.nom).first()
            
            if not v2_m:
                v2_m = models_v2.MunicipiLifecycle(
                    id=uuid.uuid4(),
                    nom=v1_m.nom,
                    poblacio=v1_m.poblacio,
                    etapa_actual=models_v2.EtapaFunnelEnum.research, # Default
                    temperatura=models_v2.TemperaturaEnum.fred,
                    created_at=v1_m.created_at or datetime.now()
                )
                if not dry_run:
                    db.add(v2_m)
                    db.flush() # Per obtenir l'ID si no el forçem
                
                logger.info(f"Municipi migrat: {v1_m.nom} ({v1_m.id} -> {v2_m.id})")
            else:
                logger.warning(f"Municipi ja existeix a V2: {v1_m.nom}. Saltant creació però mapejant ID.")
            
            municipi_mapping[v1_m.id] = v2_m.id
            
            # Crear nota_manual si hi ha notes
            if hasattr(v1_m, 'notes') and v1_m.notes:
                activitat = models_v2.ActivitatsMunicipi(
                    municipi_id=v2_m.id,
                    tipus_activitat=models_v2.TipusActivitat.nota_manual,
                    notes_comercial=v1_m.notes,
                    data_activitat=v1_m.created_at or datetime.now()
                )
                if not dry_run:
                    db.add(activitat)
            
            # Crear MemoriaMunicipi buida (només si no l'hem processat en aquesta sessió o ja existeix)
            if v2_m.id not in processed_v2_municipis:
                memoria = db.query(models_v2.MemoriaMunicipi).filter(models_v2.MemoriaMunicipi.municipi_id == v2_m.id).first()
                if not memoria:
                    memoria = models_v2.MemoriaMunicipi(
                        municipi_id=v2_m.id
                    )
                    if not dry_run:
                        db.add(memoria)
                processed_v2_municipis.add(v2_m.id)

        # 3. MIGRACIÓ CONTACTES
        logger.info("Iniciant migració de Contactes...")
        v1_contactes = db.query(models.Contacte).all()
        logger.info(f"Trobats {len(v1_contactes)} contactes a V1.")
        
        for v1_c in v1_contactes:
            v2_municipi_id = municipi_mapping.get(v1_c.municipi_id)
            if not v2_municipi_id:
                logger.error(f"Contacte {v1_c.nom} no té municipi mapejat (V1_municipi_id: {v1_c.municipi_id}). Saltant.")
                continue
                
            # Crear V2 Contacte
            v2_c = models_v2.ContacteV2(
                id=uuid.uuid4(),
                municipi_id=v2_municipi_id,
                nom=v1_c.nom,
                email=v1_c.email,
                telefon=v1_c.telefon,
                carrec=v1_c.carrec if hasattr(v1_c, 'carrec') and v1_c.carrec in models_v2.CarrecEnum.__members__ else models_v2.CarrecEnum.altre,
                principal=v1_c.principal if hasattr(v1_c, 'principal') else False,
                created_at=v1_c.created_at or datetime.now()
            )
            if not dry_run:
                db.add(v2_c)
                db.flush()
                
                # Actualitzar actor_principal_id si cal
                if v2_c.principal:
                    m_to_update = db.query(models_v2.MunicipiLifecycle).get(v2_municipi_id)
                    if m_to_update:
                        m_to_update.actor_principal_id = v2_c.id
            
            contacte_mapping[v1_c.id] = v2_c.id
            logger.info(f"Contacte migrat: {v1_c.nom} del municipi V2 {v2_municipi_id}")
            
            # Migrar notes de contacte a activitats si n'hi ha
            if hasattr(v1_c, 'notes_humanes') and v1_c.notes_humanes:
                act_c = models_v2.ActivitatsMunicipi(
                    municipi_id=v2_municipi_id,
                    contacte_id=v2_c.id,
                    tipus_activitat=models_v2.TipusActivitat.nota_manual,
                    notes_comercial=f"Nota contacte: {v1_c.notes_humanes}",
                    data_activitat=v1_c.created_at or datetime.now()
                )
                if not dry_run:
                    db.add(act_c)

        # 4. MIGRACIÓ EMAILS
        logger.info("Iniciant migració d'Emails (V1 -> V2)...")
        v1_emails = db.query(models.Email).all()
        logger.info(f"Trobats {len(v1_emails)} emails a V1.")
        
        for v1_e in v1_emails:
            # Necessitem el municipi_id. V1 Email -> Deal -> Municipi
            v1_deal = db.query(models.Deal).get(v1_e.deal_id) if v1_e.deal_id else None
            if not v1_deal:
                logger.warning(f"Email {v1_e.id} no té deal associat a V1. Saltant.")
                continue
            
            v2_municipi_id = municipi_mapping.get(v1_deal.municipi_id)
            if not v2_municipi_id:
                logger.warning(f"Email {v1_e.id} apunta a un municipi V1 no mapejat {v1_deal.municipi_id}.")
                continue
                
            # Crear EmailV2
            v2_e = models_v2.EmailV2(
                id=uuid.uuid4(),
                municipi_id=v2_municipi_id,
                contacte_id=contacte_mapping.get(v1_e.contacte_id),
                assumpte=v1_e.assumpte,
                cos=v1_e.cos,
                direccio="sortida" if v1_e.direccio in ["sortida", "OUT"] else "entrada",
                tracking_token=v1_e.tracking_token,
                created_at=v1_e.created_at or datetime.now()
            )
            
            # Crear Activitat
            activitat_e = models_v2.ActivitatsMunicipi(
                municipi_id=v2_municipi_id,
                contacte_id=v2_e.contacte_id,
                tipus_activitat=models_v2.TipusActivitat.email_enviat if v1_e.direccio in ["sortida", "OUT"] else models_v2.TipusActivitat.email_rebut,
                data_activitat=v1_e.created_at or datetime.now(),
                contingut={
                    "email_id": str(v2_e.id),
                    "assumpte": v2_e.assumpte,
                    "preview": (v2_e.cos[:100] + "...") if v2_e.cos else ""
                }
            )
            
            if not dry_run:
                db.add(v2_e)
                db.add(activitat_e)

        # 5. MIGRACIÓ TRUCADES (V2 Existing -> Activitats)
        # NOTA: Suposem que TRUCADES ja estan a V2 TrucadaV2 i volem reflectir-les a ActivitatsMunicipi
        # segons el checklist: "Migrar trucada_v2 -> activitats_municipi"
        logger.info("Migrant dades de trucada_v2 a activitats_municipi...")
        # Hem de comprovar si la taula trucada_v2 existeix/té registres
        try:
            v2_trucades = db.query(models_v2.TrucadaV2).all()
            for t in v2_trucades:
                # Evitem duplicats a activitats
                exists = db.query(models_v2.ActivitatsMunicipi).filter(
                    models_v2.ActivitatsMunicipi.contingut["trucada_id"].astext == str(t.id)
                ).first()
                if not exists:
                    act_t = models_v2.ActivitatsMunicipi(
                        municipi_id=t.municipi_id,
                        contacte_id=t.contacte_id,
                        tipus_activitat=models_v2.TipusActivitat.trucada,
                        data_activitat=t.data,
                        notes_comercial=t.notes_breus,
                        contingut={
                            "trucada_id": str(t.id),
                            "duracio_minuts": t.durada_minuts,
                            "resum_ia": t.resum_ia
                        }
                    )
                    if not dry_run:
                        db.add(act_t)
        except Exception as e:
            logger.warning(f"No s'han pogut migrar trucades_v2: {e}")

        # 6. MIGRACIÓ REUNIONS (V2 Existing -> Activitats)
        logger.info("Migrant dades de reunio_v2 a activitats_municipi...")
        try:
            v2_reunions = db.query(models_v2.ReunioV2).all()
            for r in v2_reunions:
                exists = db.query(models_v2.ActivitatsMunicipi).filter(
                    models_v2.ActivitatsMunicipi.contingut["reunio_id"].astext == str(r.id)
                ).first()
                if not exists:
                    act_r = models_v2.ActivitatsMunicipi(
                        municipi_id=r.municipi_id,
                        contacte_id=r.contacte_id,
                        tipus_activitat=models_v2.TipusActivitat.reunio, # O demo depenent de tipus
                        data_activitat=r.data,
                        notes_comercial=r.notes_aar,
                        contingut={
                            "reunio_id": str(r.id),
                            "tipus": r.tipus
                        }
                    )
                    if not dry_run:
                        db.add(act_r)
        except Exception as e:
            logger.warning(f"No s'han pogut migrar reunions_v2: {e}")

        if not dry_run:
            db.commit()
            logger.info("Migració FINALITZADA i COMMIT realitzat.")
        else:
            logger.info("FINALITZAT (Dry-run: sense canvis realitzats).")
            
    except Exception as e:
        db.rollback()
        logger.error(f"ERROR DURANT LA MIGRACIÓ: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migració de dades V1 a V2")
    parser.add_argument("--dry-run", action="store_true", help="Executa sense guardar canvis")
    parser.parse_args()
    
    args = parser.parse_args()
    migrate(dry_run=args.dry_run)
