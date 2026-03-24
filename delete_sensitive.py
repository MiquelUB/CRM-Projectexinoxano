import os
import subprocess

# Fitxers que s'han d'esborrar del disc i de Git
files_to_delete = [
    'copia_supabase_v2.sql', 'backend/copia_supabase_v2.sql',
    'copia_supabase_v3.sql', 'backend/copia_supabase_v3.sql',
    'copia_supabase_v4.sql', 'backend/copia_supabase_v4.sql',
    'dump_db.py', 'backend/restore_internal.py'
]

print("--- ESBORRANT FITXERS SENSIBLES ---")

for f in files_to_delete:
    if os.path.exists(f):
        try:
            os.remove(f)
            print(f"Esborrat localment: {f}")
        except Exception as e:
            print(f"Error esborrant {f}: {e}")

# Fer commit i push de l'esborrat a Git
print("Actualitzant GitHub...")
subprocess.run(['git', 'add', '-A'])
subprocess.run(['git', 'commit', '-m', 'Remove all sensitive database backups and restore scripts'])
res = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)

if res.returncode == 0:
    print("✅ Ajustat correctament a GitHub!")
else:
    print("❌ Error de push:")
    print(res.stderr)
