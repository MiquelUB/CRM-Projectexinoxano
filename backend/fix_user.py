import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
import auth

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def fix_user():
    db = SessionLocal()
    try:
        users = db.query(models.Usuari).all()
        print(f"Total users found: {len(users)}")
        for u in users:
            print(f"Current email in DB: {repr(u.email)}")
            print(f"Current hash in DB: {repr(u.password_hash)}")
            
            # Check if it has carriage returns or extra spaces
            if "admin@projectexinoxano.cat" in u.email:
                print("Fixing admin user...")
                u.email = "admin@projectexinoxano.cat"
                u.password_hash = auth.get_password_hash("pxx_admin_2026!")
                # Ensure active is true
                u.actiu = True
                db.commit()
                print("Admin user updated and fixed.")
                
    except Exception as e:
        print(f"Error during fixing: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_user()
