import os
import uuid
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import both sets of models
import models
import models_v2
from database import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Mapper for stages: v1 -> v2
STAGE_MAPPER = {
    "prospecte": models_v2.EtapaFunnelEnum.research,
    "contactat": models_v2.EtapaFunnelEnum.contacte,
    "demo": models_v2.EtapaFunnelEnum.demo_pendent,
    "oferta": models_v2.EtapaFunnelEnum.oferta,
    "negociacio": models_v2.EtapaFunnelEnum.aprovacio,
    "guanyat": models_v2.EtapaFunnelEnum.client,
    "perdut": models_v2.EtapaFunnelEnum.perdut,
}

def migrate():
    db = SessionLocal()
    try:
        print("Starting migration to v2...")
        
        # 1. Clear v2 tables to ensure idempotency if running multiple times (Opcional, but safe if clean start)
        db.query(models_v2.ContacteV2).delete()
        db.query(models_v2.MunicipiLifecycle).delete()
        db.commit()
        print("Cleared existing v2 tables for a clean migration.")

        # Read v1 Municipis
        v1_municipis = db.query(models.Municipi).all()
        print(f"Found {len(v1_municipis)} municipalities to migrate.")

        migrated_count = 0
        
        for m1 in v1_municipis:
            print(f"Migrating {m1.nom}...")
            
            # Find associated deal to extract lifecycle stages
            # v1 relationship: m1.deals
            deal_v1 = None
            if m1.deals:
                # Get the most recent or active deal (usually single per municipality right now)
                deal_v1 = sorted(m1.deals, key=lambda d: d.created_at, reverse=True)[0]

            # Determine etapa_actual from deal
            etapa_v2 = models_v2.EtapaFunnelEnum.research
            blocker_v2 = models_v2.BlockerEnum.cap
            temperatura_v2 = models_v2.TemperaturaEnum.fred
            description_notes = ""
            
            if deal_v1:
                # Map stage
                v1_stage = deal_v1.etapa.lower() if deal_v1.etapa else "prospecte"
                etapa_v2 = STAGE_MAPPER.get(v1_stage, models_v2.EtapaFunnelEnum.research)
                
                # Temperature based on priority or stage
                if deal_v1.prioritat == "alta":
                    temperatura_v2 = models_v2.TemperaturaEnum.calent
                elif deal_v1.prioritat == "mitjana":
                    temperatura_v2 = models_v2.TemperaturaEnum.templat
                    
                description_notes = deal_v1.notes_humanes or ""

            # Create MunicipiLifecycle
            m2 = models_v2.MunicipiLifecycle(
                id=m1.id,  # Preserve UUID for continuity!
                nom=m1.nom,
                comarca=None, # Not explicitly defined in v1 outside strings, could extract from provincia if mapped
                poblacio=int(m1.poblacio) if m1.poblacio and m1.poblacio.isdigit() else None,
                geografia=models_v2.GeografiaEnum.interior, # Default fallback
                diagnostic_digital={
                    "web": m1.web,
                    "telefon_general": m1.telefon,
                    "adreca": m1.adreca,
                    "notes_v1": m1.notes
                },
                angle_personalitzacio=description_notes[:300] if description_notes else "Mantenir calor comercial.",
                etapa_actual=etapa_v2,
                blocker_actual=blocker_v2,
                temperatura=temperatura_v2,
                dies_etapa_actual=0,
                data_creacio=m1.created_at,
                data_ultima_accio=m1.updated_at,
            )
            
            # Map state_final if win/lost
            if etapa_v2 == models_v2.EtapaFunnelEnum.client:
                m2.estat_final = models_v2.EstatFinalEnum.client
                m2.data_conversio = deal_v1.updated_at if deal_v1 else m1.updated_at
            elif etapa_v2 == models_v2.EtapaFunnelEnum.perdut:
                m2.estat_final = models_v2.EstatFinalEnum.perdut

            db.add(m2)
            db.flush() # Secure ID being posted before creating children just in case

            # Migrate Contactes for this municipality
            principal_actor_id = None
            
            for c1 in m1.contactes:
                # Map carrec
                carrec_v2 = models_v2.CarrecEnum.altre
                if c1.carrec:
                    c_lower = c1.carrec.lower()
                    if "alcalde" in c_lower:
                        carrec_v2 = models_v2.CarrecEnum.alcalde
                    elif "tecnic" in c_lower or "tècnic" in c_lower:
                        carrec_v2 = models_v2.CarrecEnum.tecnic
                    elif "cfo" in c_lower or "finances" in c_lower:
                        carrec_v2 = models_v2.CarrecEnum.cfo
                    elif "cultura" in c_lower:
                        carrec_v2 = models_v2.CarrecEnum.regidor_cultura
                    elif "turisme" in c_lower:
                        carrec_v2 = models_v2.CarrecEnum.regidor_turisme

                # Flag as principal if tied to the active deal contacte_id
                is_principal = False
                if deal_v1 and deal_v1.contacte_id and deal_v1.contacte_id == c1.id:
                    is_principal = True

                c2 = models_v2.ContacteV2(
                    id=c1.id,  # Preserve UUID
                    municipi_id=m2.id,
                    nom=c1.nom,
                    carrec=carrec_v2,
                    email=c1.email,
                    telefon=c1.telefon,
                    actiu=c1.actiu,
                    principal=is_principal,
                    angles_exitosos=[],
                    angles_fallits=[],
                    moment_optimal=None,
                    to_preferit=models_v2.ToComunicacioEnum.formal
                )
                db.add(c2)
                
                if is_principal:
                    principal_actor_id = c2.id

            db.flush()
            
            # Update Principal Actor FK if found
            if principal_actor_id:
                m2.actor_principal_id = principal_actor_id
                
            migrated_count += 1

        db.commit()
        print(f"\nMigration successfully completed! Migrated {migrated_count} municipalities.")

    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
