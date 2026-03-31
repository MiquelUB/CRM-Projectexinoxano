import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv("backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL not found in .env")
    exit(1)

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    try:
        # Alter column type to VARCHAR
        connection.execute(text("ALTER TABLE municipis ALTER COLUMN poblacio TYPE VARCHAR(255) USING poblacio::VARCHAR;"))
        connection.commit()
        print("Column 'poblacio' successfully changed to VARCHAR in database.")
    except Exception as e:
        print(f"Error modifying database: {e}")
