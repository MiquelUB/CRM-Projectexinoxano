import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv
import models

# Load environment variables
load_dotenv()

# LOCAL DOCKER DB (Source)
LOCAL_DB_URL = "postgresql://pxx_admin:pxx_secret_local@127.0.0.1:5433/crm_pxx"
# SUPABASE DB (Target)
REMOTE_DB_URL = os.getenv("DATABASE_URL")

def migrate_data():
    try:
        # Create engines
        local_engine = sqlalchemy.create_engine(LOCAL_DB_URL)
        remote_engine = sqlalchemy.create_engine(REMOTE_DB_URL)
        
        # Create sessions
        LocalSession = sessionmaker(bind=local_engine)
        RemoteSession = sessionmaker(bind=remote_engine)
        
        local_db = LocalSession()
        remote_db = RemoteSession()
        
        # List of models in REVERSE order for deletion
        table_chain = [
            models.Tasca,
            models.Pagament,
            models.Llicencia,
            models.Email,
            models.DealActivitat,
            models.Deal,
            models.Contacte,
            models.Municipi,
            models.Usuari
        ]
        
        print("Cleaning up remote database for a fresh migration...")
        for model in table_chain:
            try:
                # Truncate or delete
                remote_db.execute(text(f"DELETE FROM {model.__tablename__} CASCADE"))
                print(f"Cleared {model.__tablename__}")
            except Exception as e:
                print(f"Warning clearing {model.__tablename__}: {e}")
        remote_db.commit()

        # List of models in correct order for insertion
        migration_order = table_chain[::-1]
        
        for model in migration_order:
            table_name = model.__tablename__
            print(f"Migrating table: {table_name}...")
            
            items = local_db.query(model).all()
            print(f"Found {len(items)} records in {table_name}.")
            
            for item in items:
                try:
                    local_db.expunge(item)
                    sqlalchemy.orm.make_transient(item)
                    remote_db.add(item)
                except Exception as e:
                    print(f"Error adding item to {table_name}: {e}")
            
            remote_db.commit()
            print(f"Table {table_name} migrated successfully.")
            
        print("\nSUCCESS: ALL DATA MIGRATED TO SUPABASE!")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        local_db.close()
        remote_db.close()

if __name__ == "__main__":
    migrate_data()
