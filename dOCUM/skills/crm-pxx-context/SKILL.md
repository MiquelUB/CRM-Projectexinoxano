---
name: crm-pxx-context
description: Provides full project context for the CRM Projecte Xino Xano (PXX). Use this skill at the start of every task related to the CRM PXX codebase. Contains business model, tech stack, data model, and all architectural decisions.
---

# CRM PXX — Context Global del Projecte

Llegeix aquest skill SEMPRE que treballis en qualsevol part del CRM de Projecte Xino Xano.

## Qui és PXX?

Projecte Xino Xano (PXX) és una empresa SaaS B2G (Business to Government) que ven llicències de turisme digital a Ajuntaments i Diputacions provincials. El seu producte és una app de turisme de marca blanca amb sobirania digital (sense Google Maps, sense dependències externes de pagament).

## Model de Negoci

- **Clients objectiu:** Ajuntaments i Diputacions provincials (Espanya, principalment Catalunya)
- **Ticket promig:** Setup Fee 3.500€–15.000€ + Llicència Anual 1.800€–10.000€
- **Cicle de venda:** Llarg (3–12 mesos). Decisió política + tramitació administrativa.
- **Pagaments:** Exclusivament per transferència bancària. Cap passarel·la de pagament.
- **Estratègia comercial clau:** Venda a Diputacions (cobreix 15 municipis en un sol contracte).

## Stack Tecnològic (NO modificar sense justificació)

- **Backend:** FastAPI (Python 3.11+) + SQLAlchemy ORM
- **Base de Dades:** PostgreSQL 15 + extensió PostGIS
- **Frontend:** Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui
- **Autenticació:** JWT (python-jose) + bcrypt (passlib) — tokens de 24h
- **IA:** OpenRouter API — model flexible, es tria per tasca en temps d'execució
- **Correu:** IMAP/SMTP via imaplib Python — compte @projectexinoxano.cat (CDmon)
- **Infraestructura:** VPS propi + Docker Compose + Nginx reverse proxy
- **Desenvolupament local:** PostgreSQL via Docker Compose al port 5432

## Principi Rector: Sobirania Digital

Cap dada del CRM surt del servidor propi de PXX. No s'utilitzen serveis de tercers per emmagatzemar informació de clients (sense HubSpot, sense Salesforce, sense Google Workspace com a BD). Coherent amb la proposta de valor que PXX ven als seus clients.

## Model de Dades — 8 Taules

```
usuaris         → Login i autenticació
municipis       → Ajuntaments i Diputacions (clients potencials)
contactes       → Persones de contacte dins cada municipi
deals           → Oportunitats comercials al pipeline
llicencies      → Contractes SaaS actius (1:1 amb deal tancat)
pagaments       → Registre de transferències bancàries
emails          → Tots els emails IN i OUT vinculats a deals
campanyes       → Seqüències d'email màrqueting híbrides
tasques         → Tasques comercials i de desenvolupament intern
```

## Regles Crítiques (mai trencar)

1. **Tots els IDs són UUID** — mai integers autoincrement
2. **Tots els models tenen** `created_at` i `updated_at` (TIMESTAMPTZ, DEFAULT NOW())
3. **El camp `etapa` dels deals** accepta NOMÉS: `prospecte` | `contacte_inicial` | `demo_feta` | `proposta_enviada` | `tramitacio_admin` | `tancat_guanyat` | `perdut`
4. **Notes humanes = text lliure** — mai etiquetes, mai puntuacions numèriques
5. **Mai secrets al codi** — sempre variables d'entorn via `.env`
6. **Missatges d'error de l'API en català**
7. **Dades de prova amb municipis catalans reals** (Lleida, Tarragona, Girona, Barcelona, etc.)
8. **OpenAI mai** — sempre OpenRouter per a qualsevol integració d'IA

## Estructura de Carpetes

```
crm-pxx/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── municipis.py
│   │   ├── contactes.py
│   │   ├── deals.py
│   │   ├── emails.py
│   │   ├── campanyes.py
│   │   ├── pagaments.py
│   │   └── tasques.py
│   └── .env
├── frontend/
│   ├── app/
│   │   ├── dashboard/
│   │   ├── municipis/
│   │   ├── contactes/
│   │   ├── deals/
│   │   ├── emails/
│   │   └── login/
│   ├── components/
│   └── lib/api.ts
└── docker-compose.yml
```
