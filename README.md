# Projecte Xino Xano CRM (CRM PXX)

La plataforma intel·ligent i centralitzada per a la gestió de pipeline comercial, municipis i llicències.

---

## 🚀 Arquitectura del Projecte

El projecte està dividit en dues parts principals:

1. **/backend**: API de FastAPI (Python) que gestiona la base de dades (PostgreSQL via Supabase), l'autenticació, la lògica de negoci i els serveis d'IA (OpenRouter).
2. **/frontend**: Aplicació en Next.js (React) que utilitza TailwindCSS per a una interfície d'usuari moderna, tauler de control Kanban i seguiments d'email.

---

## 🛠️ Requisits previs
- **Python 3.10+** (per al backend)
- **Node.js 18+** i **npm** (per al frontend)
- Base de dades **PostgreSQL** (amb supòsit de Postgres Supabase lligat al `.env`)

---

## 📥 Instal·lació i Configuració

### 1. Backend (FastAPI)

Entra a la carpeta de backend:
```bash
cd backend
```

Crea un entorn virtual i activa'l:
- **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

Instal·la les dependències:
```bash
pip install -r requirements.txt
```

#### ⚙️ Configuració del Backend (`.env`)
Assegura't de tenir un arxiu `.env` a la carpeta `backend` amb les següents variables (adapta-les al teu entorn):
```env
DATABASE_URL=postgresql://usuari:contrasenya@host:port/bd
SECRET_KEY=la_teva_clau_secreta_llarga
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Integració AI (OpenRouter)
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Emails (IMAP/SMTP)
IMAP_HOST=imap.exinoxano.cat
IMAP_PORT=993
SMTP_HOST=smtp.exinoxano.cat
SMTP_PORT=465
```

Inicia el servidor:
```bash
uvicorn main:app --reload
```
*L'API estarà disponible a [http://127.0.0.1:8000](http://127.0.0.1:8000)*

---

### 2. Frontend (Next.js)

Entra a la carpeta de frontend:
```bash
cd ../frontend
```

Instal·la els mòduls de Node:
```bash
npm install
```

#### ⚙️ Configuració del Frontend (`.env.local`)
Crea un arxiu `.env.local` si no existeix:
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Inicia el servidor de desenvolupament:
```bash
npm run dev
```
*L'aplicació estarà disponible a [http://localhost:3000](http://localhost:3000)*

---

## 🌟 Característiques Principals

### 🏢 Gestió de Municipis i Contactes
- Base de dades de municipis (ajuntaments, diputacions).
- Fitxa detallada de contactes amb càrrec, mail i notes.

### 📋 Kanban Pipeline (Deals)
- Gestió visual de deals per etapes (`prospecte`, `reunio_feta`, `oferta_enviada`, `guanyat`, `perdut`).
- Suporta "Drag-and-Drop" per moure les fitxes entre columnes.

### 🤖 Agent d'Intel·ligència Artificial
- Redacció automàtica de correus corporatius basant-se en l'estat del deal.
- Anàlisi i resum de deals per a la presa de decisions comercials.

### 📬 Gestió de Correu Electrònic i Seguiment
- Sincronització de correus interns/externs amb els contactes lligats a un municipi.
- *Email Open Tracking* per veure estadístiques d'obertura dels missatges.

### 💳 Llicències i Pagaments
- Gestió d'estat de llicències (activa, cancel·lada, suspesa) vinculades a Deals.
- Seguiment de pagaments (setup fee, llicència anual), dates de venciment i imports.
- KPI summaries al dashboard.

---

## 🐳 Docker (Opcional)
Si utilitzes el `docker-compose.yml` del repositori per a servicis addicionals (com un PostgreSQL local de proves):
```bash
docker-compose up -d
```
