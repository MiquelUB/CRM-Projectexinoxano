import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_user():
    db = SessionLocal()
    target_email = "admin@projectexinoxano.cat"
    user = db.query(models.Usuari).filter(models.Usuari.email == target_email).first()
    
    if user:
        print(f"Email: {repr(user.email)}")
        print(f"Role: {repr(user.rol)}")
        print(f"Nom: {repr(user.nom)}")
        print(f"Password hash: {repr(user.password_hash)}")
    else:
        print("User not found.")
    db.close()

if __name__ == "__main__":
    check_user()
