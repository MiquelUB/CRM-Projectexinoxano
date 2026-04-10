import logging
from database import engine
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)

def force_sync_v2():
    with engine.connect() as conn:
        # Afegeix TOTA columna que pugui faltar per evitar el 500
        columnes = [
            "data_ultima_accio TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP",
            "municipi_v1_id UUID",
            "actor_principal_id UUID",
            "comarca VARCHAR(50)",
            "poblacio VARCHAR(100)",
            "diagnostic_digital JSONB DEFAULT '{}'::jsonb",
            "angle_personalitzacio TEXT",
            "historial_etapes JSONB DEFAULT '[]'::jsonb",
            "dies_etapa_actual INTEGER DEFAULT 0",
            "data_conversio TIMESTAMP WITH TIME ZONE",
            "usuari_asignat VARCHAR(50) DEFAULT 'fundador'",
            "etapa_actual VARCHAR(50) DEFAULT 'research'",
            "blocker_actual VARCHAR(50) DEFAULT 'cap'",
            "temperatura VARCHAR(50) DEFAULT 'fred'",
            "pla_contractat VARCHAR(50)",
            "estat_final VARCHAR(50)",
            "geografia VARCHAR(50)"
        ]
        
        for col in columnes:
            col_name = col.split()[0]
            try:
                # El IF NOT EXISTS evita errors si la columna ja hi és
                conn.execute(text(f"ALTER TABLE municipis_lifecycle ADD COLUMN IF NOT EXISTS {col};"))
                print(f"✅ Columna garantida: {col_name}")
            except Exception as e:
                print(f"⚠️ Nota sobre {col_name}: {e}")
        
        conn.commit()
        print("🚀 Base de dades purgada i sincronitzada!")

if __name__ == "__main__":
    force_sync_v2()
