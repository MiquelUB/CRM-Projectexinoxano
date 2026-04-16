
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import logging
from datetime import datetime, timezone, timedelta

from services.email_sync import sync_all_emails
from services.alertes import process_alertes_diaries

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

def daily_maintenance():
    """Manteniment diari: Neteja de memòria i actualització d'estats."""
    from database import SessionLocal
    import models
    logger.info("Executant manteniment diari...")
    db = SessionLocal()
    try:
        # Aquí es poden afegir rutines de neteja
        pass
    except Exception as e:
        logger.error(f"Error manteniment: {e}")
    finally:
        db.close()

def start_scheduler():
    logger.info("Configuring Unified APScheduler jobs...")
    
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
        name="Check alerts at 8AM",
        replace_existing=True
    )

    scheduler.add_job(
        daily_maintenance,
        trigger=CronTrigger(hour=6, minute=0),
        id="daily_maint",
        name="Daily system maintenance at 6AM",
        replace_existing=True
    )

    scheduler.start()
    logger.info("APScheduler started.")

def shutdown_scheduler():
    scheduler.shutdown()
    logger.info("APScheduler stopped.")
