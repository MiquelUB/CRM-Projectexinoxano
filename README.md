# Projecte Xino Xano CRM (CRM PXX)

La plataforma intel·ligent i centralitzada per a la gestió de pipeline comercial, municipis i llicències.

---

## 🚀 Arquitectura del Projecte

El projecte està dividit en dues parts principals:

1. **/backend**: API de FastAPI (Python) que gestiona la base de dades (PostgreSQL a Easypanel), l'autenticació, la lògica de negoci unificada i els serveis d'IA (OpenRouter).
2. **/frontend**: Aplicació en Next.js (React) que utilitza TailwindCSS per a una interfície d'usuari moderna, tauler de control Kanban i seguiments d'email.

---

## 🏗️ Estat del Projecte i Nova Arquitectura V2

El sistema s'executa ara sota l'arquitectura unificada iterada en **V2**.
- **Model de Lifecycle**: S'utilitza la taula global `municipis_lifecycle` consolidant el pipeline sencer (Lead, Prospect, Demo, Negociació, Closed Won).
- **Activitat (Timeline)**: El nou model `activitats_municipi` actua com a single source of truth cronològic (emails, reunions, trucades, notes lliures) facilitant un *Scroll Infinit* fluid en la interífice gràfica.
- **Mission Control**: Tauler complet d'intel·ligència i visibilitat de municipis amb accés a gràfiques de recorregut i edició global in-line.
- **Agent Kimi K2**: Un sistema d'assistent intel·ligent ("chat global" & "sidebar") amb memoria tàctica (Base de dades jeràrquica), auto-anàlisi de silencis/bloquejos, poling asíncron i sugestions guiades on-the-fly (`accions_suggerides`).
- **Prompts Dinàmics**: Sistema centralitzat d'entrenament (`backend/config/prompts.yaml`) recarregable en calenta basat en YAML+Jinja2.

---

## 🛠️ Requisits previs
- **Python 3.11+**
- **Node.js 18+** i **npm**
- **PostgreSQL 15+** (Self-hosted o via Easypanel)

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

Instal·la les dependències:
```bash
pip install -r requirements.txt
```

#### ⚙️ Configuració del Backend (`.env`)
```env
DATABASE_URL=postgresql://usuari:contrasenya@178.104.83.189:5432/crm_pxx
SECRET_KEY=...
# Integració AI
OPENROUTER_API_KEY=...
```

---

## 🌟 Característiques V2

### 🏢 Lifecycle de Municipi Unificat
- Gestió de tot el funnel des de la fitxa del municipi.
- Historial d'accions cronològic (timeline).

### 🤖 Kimi K2 AI (Prompts Dinàmics)
- La personalitat i habilitats de l'IA es defineixen a `config/prompts.yaml`.
- Suport per a canvis en calent sense reiniciar el servidor.

### 📊 Dashboard de KPIs V2
- Endpoints optimitzats a `/api/dashboard` i `/api/municipis_lifecycle/kpis`.

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
