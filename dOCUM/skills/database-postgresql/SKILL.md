---
name: database-postgresql
description: Guides PostgreSQL schema design, migrations with Alembic, and query optimization for CRM PXX. Use when creating new tables, modifying existing schema, writing complex queries, or managing database migrations.
---

# PostgreSQL — Convencions CRM PXX

Aplica aquest skill sempre que treballis amb la base de dades.

## Connexió Local (Docker)

```bash
# Iniciar BD
docker-compose up -d

# Connectar-se directament
psql -h localhost -U pxx_admin -d crm_pxx

# Verificar taules existents
\dt

# Parar BD
docker-compose down
```

## Migracions amb Alembic

```bash
# Inicialitzar Alembic (només una vegada)
cd backend
alembic init migrations

# Crear nova migració (després de canviar models.py)
alembic revision --autogenerate -m "descripcio_del_canvi"

# Aplicar migracions pendents
alembic upgrade head

# Veure historial
alembic history

# Revertir última migració (amb precaució)
alembic downgrade -1
```

## Regles d'Esquema

```sql
-- UUID per defecte (SEMPRE, mai SERIAL)
id UUID PRIMARY KEY DEFAULT gen_random_uuid()

-- Timestamps (SEMPRE en tots els models)
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

-- Foreign Keys amb comportament explícit
municipi_id UUID NOT NULL REFERENCES municipis(id) ON DELETE RESTRICT

-- Enums com VARCHAR amb CHECK (més flexible que tipus ENUM)
etapa VARCHAR(50) NOT NULL DEFAULT 'prospecte'
  CHECK (etapa IN ('prospecte','contacte_inicial','demo_feta',
                   'proposta_enviada','tramitacio_admin',
                   'tancat_guanyat','perdut'))
```

## Índexs Obligatoris

Crea sempre aquests índexs per al rendiment:

```sql
-- Cerca per municipi (molt freqüent)
CREATE INDEX idx_deals_municipi_id ON deals(municipi_id);
CREATE INDEX idx_contactes_municipi_id ON contactes(municipi_id);

-- Filtre per etapa al Kanban
CREATE INDEX idx_deals_etapa ON deals(etapa);

-- Emails per deal (consultat sempre al detall)
CREATE INDEX idx_emails_deal_id ON emails(deal_id);

-- Renovacions properes (alerta automàtica)
CREATE INDEX idx_llicencies_data_renovacio ON llicencies(data_renovacio);

-- Pagaments vençuts
CREATE INDEX idx_pagaments_estat ON pagaments(estat);
```

## Trigger per updated_at

Crea aquest trigger un sol cop i aplica'l a totes les taules:

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar a cada taula nova:
CREATE TRIGGER update_municipis_updated_at
  BEFORE UPDATE ON municipis
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## Queries Freqüents del CRM

```sql
-- KPIs del pipeline
SELECT etapa, COUNT(*) as total,
       SUM(valor_setup + valor_llicencia) as valor_total
FROM deals
WHERE etapa != 'perdut'
GROUP BY etapa;

-- Renovacions properes (30 dies)
SELECT l.*, m.nom as municipi_nom
FROM llicencies l
JOIN deals d ON l.deal_id = d.id
JOIN municipis m ON d.municipi_id = m.id
WHERE l.data_renovacio BETWEEN NOW() AND NOW() + INTERVAL '30 days'
AND l.estat = 'activa';

-- Deals sense activitat (14+ dies)
SELECT d.*, m.nom as municipi_nom
FROM deals d
JOIN municipis m ON d.municipi_id = m.id
WHERE d.updated_at < NOW() - INTERVAL '14 days'
AND d.etapa NOT IN ('tancat_guanyat', 'perdut');
```

## Backup Manual

```bash
# Backup complet
pg_dump -h localhost -U pxx_admin crm_pxx > backup_$(date +%Y%m%d).sql

# Restaurar
psql -h localhost -U pxx_admin crm_pxx < backup_20260101.sql
```
