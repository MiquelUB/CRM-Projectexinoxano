from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import logging

from services.email_sync import sync_all_emails
from services.alertes import process_alertes_diaries

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

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
    
    scheduler.start()
    logger.info("APScheduler started.")

def shutdown_scheduler():
    scheduler.shutdown()
    logger.info("APScheduler stopped.")
