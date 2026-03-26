#!/bin/bash
echo "Corregint permisos de la base de dades abans que Alembic falli..."
python fix_schema.py

echo "Executant migracions d'Alembic..."
python -m alembic upgrade head

echo "Iniciant FastAPI..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000
