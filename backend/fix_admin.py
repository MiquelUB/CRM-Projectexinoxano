import os
import sys
import bcrypt

# Add current dir to path
sys.path.append(os.getcwd())

from database import SessionLocal
import models
from auth import get_password_hash

def fix_user():
    db = SessionLocal()
    email = "admin@projectexinoxano.cat"
    new_password = "pxx_admin_2026!"
    
    try:
        user = db.query(models.Usuari).filter(models.Usuari.email == email).first()
        
        if user:
            print(f"User {email} found. Resetting password and ensuring active status...")
            user.password_hash = get_password_hash(new_password)
            user.actiu = True
            user.rol = "admin"
            db.commit()
            print("User updated successfully.")
        else:
            print(f"User {email} not found. Creating user...")
            new_user = models.Usuari(
                email=email,
                password_hash=get_password_hash(new_password),
                nom="Administrador",
                rol="admin",
                actiu=True
            )
            db.add(new_user)
            db.commit()
            print("User created successfully.")
            
    except Exception as e:
        print(f"ERROR: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_user()
