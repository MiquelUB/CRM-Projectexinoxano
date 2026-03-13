import os
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import Pagament, Llicencia

logger = logging.getLogger(__name__)

def process_alertes_diaries():
    logger.info("Executing process_alertes_diaries...")
    db = SessionLocal()
    today = datetime.now().date()
    
    try:
        target_date = today + timedelta(days=30)
        llicencies_properes = db.query(Llicencia).filter(
            Llicencia.data_renovacio == target_date,
            Llicencia.estat == 'activa'
        ).all()
        
        for llic in llicencies_properes:
            existeix = db.query(Pagament).filter(
                Pagament.llicencia_id == llic.id,
                Pagament.tipus == 'llicencia_anual',
                Pagament.estat.in_(['proper', 'emes'])
            ).first()
            
            if not existeix:
                last_pag = db.query(Pagament).filter(
                    Pagament.llicencia_id == llic.id,
                    Pagament.tipus == 'llicencia_anual',
                    Pagament.estat == 'confirmat'
                ).order_by(Pagament.data_confirmacio.desc()).first()
                
                import_renovacio = last_pag.import_ if last_pag else 3500.00
                
                nou_pagament = Pagament(
                    llicencia_id=llic.id,
                    import_=import_renovacio,
                    tipus="llicencia_anual",
                    estat="proper",
                    data_emisio=today,
                    data_limit=llic.data_renovacio
                )
                db.add(nou_pagament)
                logger.info(f"Creat pagament proper per a llicència {llic.id}")
                
        data_limit_emes = today - timedelta(days=15)
        pagaments_obsolets = db.query(Pagament).filter(
            Pagament.estat == 'emes',
            Pagament.data_emisio < data_limit_emes
        ).all()
        
        for pag in pagaments_obsolets:
            pag.estat = "vencut"
            logger.info(f"Pagament {pag.id} marcat com a vencut (15 dies d'emissió).")
            
        pagaments_passats = db.query(Pagament).filter(
            Pagament.estat.in_(['emes', 'proper']),
            Pagament.data_limit < today
        ).all()
        
        for pag in pagaments_passats:
            pag.estat = "vencut"
            logger.info(f"Pagament {pag.id} marcat com a vencut (Data límit superada).")
            
        db.commit()
        
    except Exception as e:
        logger.error(f"Error a process_alertes_diaries: {e}")
        db.rollback()
    finally:
        db.close()
