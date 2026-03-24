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
    
    with open("db_user_inspect.txt", "w") as f:
        if user:
            f.write(f"Email: {repr(user.email)}\n")
            f.write(f"Role: {repr(user.rol)}\n")
            f.write(f"Nom: {repr(user.nom)}\n")
            f.write(f"Password hash: {repr(user.password_hash)}\n")
        else:
            f.write("User not found.\n")
            
    db.close()

if __name__ == "__main__":
    check_user()
