import asyncio
from main import app
from database import SessionLocal
import models
import scheduler

async def test_startup():
    print("Testing application startup...")
    try:
        # Manually trigger lifespan-like logic
        scheduler.start_scheduler()
        print("Scheduler started.")
        
        db = SessionLocal()
        count = db.query(models.Usuari).count()
        print(f"Database reachable. User count: {count}")
        db.close()
        
        print("Startup logic seems OK.")
        scheduler.shutdown_scheduler()
    except Exception as e:
        print(f"STARTUP ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_startup())
