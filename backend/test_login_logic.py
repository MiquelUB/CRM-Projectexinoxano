import sys
import os
from dotenv import load_dotenv

# Add backend directory to path
sys.path.append(os.path.abspath('.'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
from routers.auth import login
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

load_dotenv()

# Mocking OAuth2PasswordRequestForm
class FormMock:
    def __init__(self, username, password):
        self.username = username
        self.password = password

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_login():
    db = SessionLocal()
    try:
        mock_form = FormMock(username="admin@projectexinoxano.cat", password="pxx_admin_2026!")
        print("Testing login logic...")
        res = login(form_data=mock_form, db=db)
        print("Login outcome:")
        print(res)
    except Exception as e:
        print(f"Login failed logic: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_login()
