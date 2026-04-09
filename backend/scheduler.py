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

def cleanup_expired_sessions():
    """Elimina sessions de xat (Nivell 1) que han expirat."""
    from database import SessionLocal
    from models_v2 import AgentMemoryV2
    from datetime import datetime, timezone
    logger.info("Executant neteja de sessions de xat expirades...")
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        deleted = db.query(AgentMemoryV2).filter(
            AgentMemoryV2.session_id.isnot(None),
            AgentMemoryV2.expires_at < now
        ).delete()
        db.commit()
        if deleted > 0:
            logger.info(f"S'han eliminat {deleted} sessions expirades.")
    except Exception as e:
        logger.error(f"Error cleanup_expired_sessions: {e}")
    finally:
        db.close()

def weekly_tactical_aggregation():
    """Genera el resum setmanal (Nivell 2) per a cada municipi."""
    from database import SessionLocal
    from services.memory_engine import memory_engine
    logger.info("Executant agregació tàctica setmanal...")
    db = SessionLocal()
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(memory_engine.run_weekly_aggregation(db))
        loop.close()
    except Exception as e:
        logger.error(f"Error weekly_tactical_aggregation: {e}")
    finally:
        db.close()

def monthly_strategic_learning():
    """Analitza patrons globals (Nivell 3) mensualment."""
    from database import SessionLocal
    from services.memory_engine import memory_engine
    logger.info("Executant aprenentatge estratègic mensual...")
    db = SessionLocal()
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(memory_engine.run_monthly_strategic_learning(db))
        loop.close()
    except Exception as e:
        logger.error(f"Error monthly_strategic_learning: {e}")
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
        cleanup_expired_sessions,
        trigger=CronTrigger(hour=3, minute=0),
        id="session_cleanup",
        name="Neteja de sessions de xat a les 3AM",
        replace_existing=True
    )

    scheduler.add_job(
        weekly_tactical_aggregation,
        trigger=CronTrigger(day_of_week='mon', hour=0, minute=0),
        id="weekly_memory",
        name="Agregació tàctica setmanal Dilluns 00:00",
        replace_existing=True
    )

    scheduler.add_job(
        monthly_strategic_learning,
        trigger=CronTrigger(day=1, hour=1, minute=0),
        id="monthly_learning",
        name="Aprenentatge estratègic mensual dia 1 a la 1AM",
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
