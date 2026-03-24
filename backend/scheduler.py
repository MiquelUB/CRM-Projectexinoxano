from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import logging

from services.email_sync import sync_all_emails
from services.alertes import process_alertes_diaries

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

def daily_memory_cleanup():
    """Actualitza el temps de cicle i dades dels municipis."""
    from database import SessionLocal
    from models_v2 import MunicipiLifecycle
    from services.memory_engine import update_municipi_memory
    logger.info("Executant memory cleanup diari...")
    db = SessionLocal()
    try:
        municipis = db.query(MunicipiLifecycle).all()
        for m in municipis:
             update_municipi_memory(db, str(m.id))
    except Exception as e:
         logger.error(f"Error memory cleanup: {e}")
    finally:
         db.close()

def job_preparar_emails_sequencia():
    """Genera drafts per a les seqüències pendents reservades per avui."""
    from database import SessionLocal
    from models_v2 import EmailSequenciaV2, EstatSequenciaEnum
    from services.sequenciador import preparar_email_sequencia
    from datetime import datetime
    logger.info("Executant preparació d'emails de seqüència...")
    db = SessionLocal()
    try:
        avui = datetime.utcnow().date()
        pendents = db.query(EmailSequenciaV2).filter(
            EmailSequenciaV2.estat == EstatSequenciaEnum.pendent
        ).all()
        for seq in pendents:
            if seq.data_programada.date() <= avui:
                # El mètode és async, per tant cal cridar-lo des d'un event loop o fer-lo síncron
                # Atès que apscheduler és async de fons per AsyncIOScheduler, les nostres funcions són regulars.
                # Per tal de simplificar o d'executar-lo:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(preparar_email_sequencia(db, seq.municipi_id, seq.numero_email))
                loop.close()
    except Exception as e:
        logger.error(f"Error preparar_emails_sequencia: {e}")
    finally:
        db.close()

def start_scheduler():
    logger.info("Configuring APScheduler jobs...")
    
    scheduler.add_job(
        sync_all_emails,
        trigger=IntervalTrigger(minutes=5),
        id="sync_emails",
        name="Sync IMAP emails every 5 mins",
        replace_existing=True
    )
    
    scheduler.add_job(
        process_alertes_diaries,
        trigger=CronTrigger(hour=8, minute=0),
        id="check_alertes",
        name="Check pagaments vencuts i renovacions a les 8AM",
        replace_existing=True
    )

    scheduler.add_job(
        daily_memory_cleanup,
        trigger=CronTrigger(hour=6, minute=0),
        id="daily_memory_cleanup",
        name="Update MunicipiLifecycle daily timers at 6AM",
        replace_existing=True
    )

    scheduler.add_job(
        job_preparar_emails_sequencia,
        trigger=CronTrigger(hour=8, minute=30),
        id="preparar_emails_sequencia",
        name="Update/Draft sequences for today at 8:30AM",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("APScheduler started.")

def shutdown_scheduler():
    scheduler.shutdown()
    logger.info("APScheduler stopped.")
