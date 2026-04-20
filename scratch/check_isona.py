import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from database import engine
from sqlalchemy import text

def check_isona():
    with engine.connect() as conn:
        print("Checking data for 'Isona i Conca Dellà'...")
        # 1. Get Municipi ID
        res = conn.execute(text("SELECT id, nom FROM municipis WHERE nom ILIKE :nom"), {"nom": "%Isona%"}).fetchall()
        if not res:
            print("No municipi found matching 'Isona'")
            return
        
        for m_id, m_name in res:
            print(f"\nMunicipi: {m_name} (ID: {m_id})")
            
            # 2. Count Contacts
            c_count = conn.execute(text("SELECT COUNT(*) FROM contactes WHERE municipi_id = :id"), {"id": m_id}).scalar()
            print(f" - Contactes: {c_count}")
            
            # 3. Count Emails
            e_count = conn.execute(text("SELECT COUNT(*) FROM emails WHERE municipi_id = :id"), {"id": m_id}).scalar()
            print(f" - Emails: {e_count}")
            
            # 4. Count Activities
            a_count = conn.execute(text("SELECT COUNT(*) FROM activitats WHERE municipi_id = :id"), {"id": m_id}).scalar()
            print(f" - Activitats: {a_count}")
            
            # 5. Check if emails have another ID or are orphaned
            if e_count == 0:
                print("   Checking for orphaned emails or old links...")
                orphaned = conn.execute(text("SELECT COUNT(*) FROM emails WHERE municipi_id IS NULL")).scalar()
                print(f"   - Total orphaned emails: {orphaned}")

if __name__ == "__main__":
    check_isona()
