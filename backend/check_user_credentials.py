import os
import bcrypt
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import models

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL not found in .env")
    exit(1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def verify_password(plain_password, hashed_password):
    try:
        password_byte_enc = plain_password.encode('utf-8')
        hashed_password_byte_enc = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)
    except Exception as e:
        print(f"Verification error: {e}")
        return False

def check_user():
    db = SessionLocal()
    try:
        target_email = "admin@projectexinoxano.cat"
        password_to_check = "pxx_admin_2026!"
        
        user = db.query(models.Usuari).filter(models.Usuari.email == target_email).first()
        
        if user:
            print(f"User found: {user.email}")
            print(f"Role: {user.rol}")
            print(f"Active: {user.actiu}")
            print(f"Password hash: {user.password_hash}")
            
            is_valid = verify_password(password_to_check, user.password_hash)
            print(f"Password verification: {'SUCCESS' if is_valid else 'FAILED'}")
        else:
            print(f"User {target_email} NOT found.")
            print("\nListing all users in DB:")
            users = db.query(models.Usuari).all()
            for u in users:
                print(f"- {u.email} (Role: {u.rol})")
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_user()
