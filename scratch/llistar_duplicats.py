import sys
import os
# Afegir el directori backend al path per poder importar models i database
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from database import engine
from sqlalchemy import text

def llistar_duplicats():
    with engine.connect() as conn:
        print("🔍 Buscant municipis duplicats per nom...")
        query = text("""
            SELECT nom, COUNT(*) 
            FROM municipis 
            GROUP BY nom 
            HAVING COUNT(*) > 1
            ORDER BY COUNT(*) DESC
        """)
        res = conn.execute(query).fetchall()
        
        if not res:
            print("✅ No s'han trobat noms duplicats.")
            return

        for nom, count in res:
            print(f"\n📌 Municipi: '{nom}' ({count} còpies)")
            # Llistar detalls de cada còpia
            details = conn.execute(text("SELECT id, etapa_actual, data_ultima_accio FROM municipis WHERE nom = :nom"), {"nom": nom}).fetchall()
            for row in details:
                print(f"   ID: {row[0]} | Etapa: {row[1]} | Última Acció: {row[2]}")

if __name__ == "__main__":
    llistar_duplicats()
