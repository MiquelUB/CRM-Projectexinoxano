FASE 1
Especificació Tècnica Completa
CRM Projecte Xino Xano
Durada: Setmanes 1–2  |  Entorn: Local  |  Mètode: Vibe Coding + IA
Versió 1.0 — Març 2026
OBJECTIU FASE 1: Un CRM funcional bàsic. Al final d'aquestes dues setmanes pots registrar municipis, contactes i deals, i moure'ls visualment pel pipeline comercial B2G. Res més, res menys.
1. Estructura del Projecte
Arquitectura monorepo local. Tot en una sola carpeta arrel per simplicitat en vibe coding.
crm-pxx/
├── backend/          ← FastAPI (Python)
│   ├── main.py       ← Punt d'entrada de l'API
│   ├── models.py     ← Models SQLAlchemy (taules BD)
│   ├── schemas.py    ← Schemas Pydantic (validació)
│   ├── routers/      ← Endpoints per mòdul
│   │   ├── municipis.py
│   │   ├── contactes.py
│   │   ├── deals.py
│   │   └── auth.py
│   ├── database.py   ← Connexió PostgreSQL
│   ├── auth.py       ← JWT logic
│   └── .env          ← Variables d'entorn (mai al git)
├── frontend/         ← Next.js 14 + TypeScript
│   ├── app/          ← App Router de Next.js
│   │   ├── dashboard/page.tsx
│   │   ├── municipis/page.tsx
│   │   ├── contactes/page.tsx
│   │   ├── deals/page.tsx
│   │   └── login/page.tsx
│   ├── components/   ← Components reutilitzables
│   │   ├── KanbanBoard.tsx
│   │   ├── DealCard.tsx
│   │   └── Sidebar.tsx
│   └── lib/api.ts    ← Client HTTP per cridar el backend
└── docker-compose.yml ← PostgreSQL local
2. Configuració de l'Entorn Local
2.1 Requisits Previs
Python 3.11+ instal·lat
Node.js 20+ instal·lat
Docker Desktop instal·lat (per a PostgreSQL local)
VS Code + extensions: Python, ESLint, Tailwind CSS IntelliSense
2.2 PostgreSQL Local via Docker
Crear el fitxer docker-compose.yml a l'arrel del projecte:
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: crm_pxx
      POSTGRES_USER: pxx_admin
      POSTGRES_PASSWORD: pxx_secret_local
    ports:
      - '5432:5432'
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
Iniciar: docker-compose up -d
2.3 Variables d'Entorn Backend (.env)
DATABASE_URL=postgresql://pxx_admin:pxx_secret_local@localhost:5432/crm_pxx
SECRET_KEY=canvia_aquest_valor_per_un_string_aleatori_llarg
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
2.4 Instal·lació Backend
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary
pip install python-jose passlib python-dotenv pydantic alembic
uvicorn main:app --reload --port 8000
2.5 Instal·lació Frontend
cd frontend
npx create-next-app@latest . --typescript --tailwind --app
npm install @tanstack/react-query axios lucide-react
npm install @dnd-kit/core @dnd-kit/sortable   # Kanban drag & drop
npx shadcn-ui@latest init
npm run dev   # Disponible a http://localhost:3000
3. Base de Dades — Esquema Complet Fase 1
Quatre taules per a la Fase 1. Totes amb camps d'auditoria (created_at, updated_at).
3.1 Taula: usuaris
Camp
Tipus
Restriccions
Descripció
id
UUID
PK, DEFAULT gen_random_uuid()
Identificador únic
email
VARCHAR(255)
UNIQUE, NOT NULL
Email de login
password_hash
VARCHAR(255)
NOT NULL
Contrasenya encriptada (bcrypt)
nom
VARCHAR(100)
NOT NULL
Nom complet de l'usuari
rol
VARCHAR(50)
DEFAULT 'admin'
Rol del sistema
actiu
BOOLEAN
DEFAULT true
Compte actiu/inactiu
created_at
TIMESTAMPTZ
DEFAULT NOW()
Data de creació
updated_at
TIMESTAMPTZ
DEFAULT NOW()
Última modificació
3.2 Taula: municipis
Camp
Tipus
Restriccions
Descripció
id
UUID
PK, DEFAULT gen_random_uuid()
Identificador únic
nom
VARCHAR(200)
NOT NULL
Nom del municipi o diputació
tipus
VARCHAR(50)
NOT NULL
Valors: 'ajuntament' | 'diputacio' | 'consell_comarcal'
provincia
VARCHAR(100)
Província on pertany
poblacio
INTEGER
Nombre d'habitants
web
VARCHAR(255)
URL web oficial
telefon
VARCHAR(50)
Telèfon principal
adreca
TEXT
Adreça postal completa
notes
TEXT
Notes lliures internes
created_at
TIMESTAMPTZ
DEFAULT NOW()
Data de creació
updated_at
TIMESTAMPTZ
DEFAULT NOW()
Última modificació
3.3 Taula: contactes
Camp
Tipus
Restriccions
Descripció
id
UUID
PK, DEFAULT gen_random_uuid()
Identificador únic
municipi_id
UUID
FK → municipis.id
Municipi al qual pertany
nom
VARCHAR(200)
NOT NULL
Nom complet
carrec
VARCHAR(200)
Càrrec oficial (ex: Alcalde, Tècnic Turisme)
email
VARCHAR(255)
Email de contacte principal
telefon
VARCHAR(50)
Telèfon directe
linkedin
VARCHAR(255)
URL perfil LinkedIn
notes_humanes
TEXT
Notes lliures de converses humanes
actiu
BOOLEAN
DEFAULT true
Contacte actiu
created_at
TIMESTAMPTZ
DEFAULT NOW()
Data de creació
updated_at
TIMESTAMPTZ
DEFAULT NOW()
Última modificació
3.4 Taula: deals
Camp
Tipus
Restriccions
Descripció
id
UUID
PK, DEFAULT gen_random_uuid()
Identificador únic
municipi_id
UUID
FK → municipis.id, NOT NULL
Municipi objectiu
contacte_id
UUID
FK → contactes.id
Persona de contacte principal
titol
VARCHAR(300)
NOT NULL
Títol descriptiu del deal
etapa
VARCHAR(50)
NOT NULL, DEFAULT 'prospecte'
Etapa actual del pipeline
valor_setup
DECIMAL(10,2)
DEFAULT 0
Import del Setup Fee (€)
valor_llicencia
DECIMAL(10,2)
DEFAULT 3500
Import llicència anual (€)
prioritat
VARCHAR(20)
DEFAULT 'mitjana'
Valors: 'alta' | 'mitjana' | 'baixa'
notes_humanes
TEXT
Notes lliures de tot el fil de conversa
proper_pas
TEXT
Camp editable: quin és el proper pas acordat
data_seguiment
DATE
Data del proper seguiment programat
data_tancament_prev
DATE
Data prevista de tancament
data_tancament_real
DATE
Data real de tancament (si s'ha tancat)
motiu_perdua
TEXT
Si etapa='perdut', per quin motiu
created_at
TIMESTAMPTZ
DEFAULT NOW()
Data de creació
updated_at
TIMESTAMPTZ
DEFAULT NOW()
Última modificació
Valors vàlids per al camp 'etapa':
Valor BD
Etiqueta Visual
Descripció
prospecte
🔵 Prospecte
Lead identificat, sense contacte inicial
contacte_inicial
📧 Contacte Inicial
Primer contacte realitzat
demo_feta
📊 Demo Feta
Presentació del producte realitzada
proposta_enviada
📄 Proposta Enviada
Document formal enviat
tramitacio_admin
⚙️ Tramitació Admin
En procés d'aprovació interna
tancat_guanyat
✅ Tancat Guanyat
Contracte signat
perdut
❌ Perdut
Deal descartat o perdut
4. Backend — Endpoints API Complets
Tots els endpoints (excepte /auth/login) requereixen header: Authorization: Bearer {token}
4.1 Autenticació — /auth
Mètode
Endpoint
Body / Params
Resposta
Descripció
POST
/auth/login
email, password
{ access_token, token_type }
Login. Retorna JWT.
POST
/auth/refresh
refresh_token
{ access_token }
Renova el token.
GET
/auth/me
—
Objecte usuari complet
Info usuari autenticat.
POST
/auth/logout
—
{ message: 'ok' }
Invalida el token.
4.2 Municipis — /municipis
Mètode
Endpoint
Body / Params
Resposta
Descripció
GET
/municipis
?page=1&limit=20&cerca=text&tipus=ajuntament
{ items[], total, page }
Llista paginada amb cerca.
GET
/municipis/{id}
—
Objecte municipi complet
Detall d'un municipi.
POST
/municipis
nom, tipus, provincia, poblacio, web, telefon, adreca, notes
Objecte municipi creat
Crear nou municipi.
PUT
/municipis/{id}
Qualsevol camp editable
Objecte municipi actualitzat
Editar municipi.
DELETE
/municipis/{id}
—
{ message: 'eliminat' }
Eliminar municipi.
GET
/municipis/{id}/deals
—
Llista de deals del municipi
Deals associats.
GET
/municipis/{id}/contactes
—
Llista de contactes
Contactes associats.
4.3 Contactes — /contactes
Mètode
Endpoint
Body / Params
Resposta
Descripció
GET
/contactes
?municipi_id=&cerca=text&page=1
{ items[], total, page }
Llista paginada.
GET
/contactes/{id}
—
Objecte contacte complet
Detall d'un contacte.
POST
/contactes
municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes
Objecte contacte creat
Crear contacte.
PUT
/contactes/{id}
Qualsevol camp editable
Objecte contacte actualitzat
Editar contacte.
DELETE
/contactes/{id}
—
{ message: 'eliminat' }
Eliminar contacte.
PATCH
/contactes/{id}/notes
notes_humanes (text lliure)
Objecte contacte actualitzat
Actualitzar notes humanes.
4.4 Deals — /deals
Mètode
Endpoint
Body / Params
Resposta
Descripció
GET
/deals
?etapa=&municipi_id=&page=1&limit=50
{ items[], total, kpis{} }
Llista amb KPIs totals.
GET
/deals/{id}
—
Objecte deal complet amb municipi i contacte
Detall complet.
POST
/deals
municipi_id, contacte_id, titol, etapa, valor_setup, valor_llicencia, prioritat, proper_pas, data_seguiment
Objecte deal creat
Crear deal.
PUT
/deals/{id}
Qualsevol camp editable
Objecte deal actualitzat
Editar deal.
PATCH
/deals/{id}/etapa
etapa (nou valor)
Objecte deal actualitzat
Canviar etapa (Kanban drag).
PATCH
/deals/{id}/notes
notes_humanes (text lliure)
Objecte deal actualitzat
Afegir/editar notes humanes.
PATCH
/deals/{id}/proper-pas
proper_pas, data_seguiment
Objecte deal actualitzat
Actualitzar proper pas.
DELETE
/deals/{id}
—
{ message: 'eliminat' }
Eliminar deal.
GET
/deals/kpis
—
{ total_deals, per_etapa{}, valor_total_pipeline }
KPIs del pipeline.
5. Frontend — Pàgines i Components
5.1 Layout General
Sidebar fixe a l'esquerra (240px) + àrea de contingut principal. El sidebar conté:
Logo PXX + nom de l'usuari autenticat.
Navegació: Dashboard, Municipis, Contactes, Deals (Pipeline), Tasques.
Indicador d'estat del servidor (online/offline) a la part inferior.
Botó de logout.
5.2 Pàgina: Login (/login)
Formulari centrat: camp email + camp password + botó 'Entrar'.
En submit: crida POST /auth/login. Si OK, guarda el JWT a httpOnly cookie i redirigeix a /dashboard.
Si error: missatge 'Credencials incorrectes' sota el formulari.
Disseny: fons fosc (#1B3A6B), targeta blanca centrada, logo PXX.
5.3 Pàgina: Dashboard (/dashboard)
4 blocs visuals en graella 2x2:
Bloc 1 — KPIs: Total Deals actius, Valor total pipeline (€), Deals per tancar aquest mes, Deals sense activitat +14 dies.
Bloc 2 — Resum Pipeline: mini-Kanban de lectura (no arrossegable). Nombre de deals per etapa.
Bloc 3 — Pròxims seguiments: llista dels 5 deals amb data_seguiment més propera.
Bloc 4 — Activitat recent: últims 10 canvis d'etapa o notes afegides (feed cronològic).
5.4 Pàgina: Pipeline Kanban (/deals)
Component principal de la Fase 1. Kanban horitzontal amb 6 columnes (una per etapa).
Cada columna mostra:
Títol de l'etapa + nombre de deals + valor total de la columna (€).
Llista de DealCards ordenades per prioritat (alta > mitjana > baixa).
Botó '+' per crear un nou deal directament en aquella etapa.
Cada DealCard mostra:
Nom del municipi (gran, destacat).
Nom del contacte principal.
Valor del deal (setup + llicència).
Indicador de prioritat (punt de color: vermell/groc/verd).
Dies en l'etapa actual.
Icona d'alerta si data_seguiment ha passat (seguiment vençut).
Clic a la targeta obre el Detall del Deal en panell lateral dret.
Drag & Drop:
Implementat amb @dnd-kit/core.
En soltar una targeta a una nova columna: crida PATCH /deals/{id}/etapa.
Actualització optimista de la UI (sense esperar resposta del servidor).
5.5 Panell Lateral: Detall del Deal
Drawer que s'obre des del Kanban al clicar una targeta. No navega a una nova pàgina.
Capçalera: Nom municipi + etapa actual + botons Editar / Tancar panell.
Secció Informació: contacte, valor setup, valor llicència, prioritat, dates.
Secció 'Proper Pas': camp de text editable + datepicker. Guardat automàtic en blur.
Secció 'Notes Humanes': textarea gran de text lliure. Historial de notes amb timestamp de quan s'han editat. Guardat amb botó explícit 'Guardar notes'.
Secció 'Historial d'Activitat': feed dels canvis d'etapa amb data i hora.
5.6 Pàgina: Municipis (/municipis)
Taula paginada amb cerca en temps real (debounce 300ms).
Columnes: Nom, Tipus, Província, Població, Deals actius (#), Accions.
Botó 'Nou Municipi' obre modal amb formulari complet.
Clic a fila obre pàgina de detall /municipis/{id} amb contactes i deals associats.
5.7 Pàgina: Contactes (/contactes)
Taula paginada amb filtre per municipi.
Columnes: Nom, Càrrec, Municipi, Email, Telèfon, Accions.
Botó 'Nou Contacte' obre modal amb formulari + selector de municipi.
Clic a fila obre detall amb les notes humanes editables i historial de deals.
6. Autenticació i Seguretat
6.1 Flux JWT
Usuari envia email + password a POST /auth/login.
Backend verifica password amb bcrypt (passlib).
Si correcte: genera JWT amb payload { sub: user_id, rol, exp: +24h }.
Frontend guarda el token en memòria (variable React) + cookie httpOnly per persistència.
Cada crida API inclou: Authorization: Bearer {token}.
Backend middleware valida el token en cada request protegit.
Si token caducat (401): frontend redirigeix automàticament a /login.
6.2 Middleware de Protecció (Next.js)
Fitxer middleware.ts a l'arrel del frontend:
Intercepta totes les rutes excepte /login.
Si no hi ha token vàlid: redirigeix a /login.
Si hi ha token: deixa passar la petició.
6.3 Encriptació de Contrasenyes
Algoritme: bcrypt amb salt rounds = 12.
Llibreria: passlib[bcrypt] (Python).
Mai s'emmagatzema la contrasenya en text pla. Mai es retorna el hash en cap endpoint.
7. Prompt de Vibe Coding per a IA
Copia i enganxa aquest prompt al teu assistent IA (Claude, Cursor, etc.) per iniciar la Fase 1:
CONTEXT DEL PROJECTE:
Estic construint un CRM a mida per a Projecte Xino Xano (PXX),
una empresa SaaS B2G que ven llicències de turisme digital a ajuntaments.
STACK TECNOLÒGIC:
- Backend: FastAPI (Python) + SQLAlchemy + PostgreSQL
- Frontend: Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui
- Auth: JWT amb python-jose + passlib bcrypt
- BD local: PostgreSQL via Docker Compose
TASCA ACTUAL — FASE 1:
Construeix [DESCRIURE LA TASCA ESPECÍFICA].
REQUISITS OBLIGATORIS:
1. Tots els IDs són UUID (no integers).
2. Tots els models tenen camps created_at i updated_at (TIMESTAMPTZ).
3. El camp 'etapa' dels deals accepta NOMÉS aquests valors:
   prospecte | contacte_inicial | demo_feta | proposta_enviada
   | tramitacio_admin | tancat_guanyat | perdut
4. Les notes_humanes són text lliure sense restriccions.
5. No generis dades de prova amb noms ficticis americans.
   Usa municipis catalans reals (Lleida, Tarragona, Girona, etc.).
6. Tots els missatges d'error de l'API han de ser en català.
7. Cap secret o credencial al codi: usa sempre variables .env.
8. Checklist de Finalització Fase 1
Marca cada punt abans de declarar la Fase 1 com a completada:
#
Ítem
Verificació
1
Docker PostgreSQL arrencat i accessible al port 5432
psql -h localhost -U pxx_admin -d crm_pxx
2
Totes les 4 taules creades (usuaris, municipis, contactes, deals)
SELECT table_name FROM information_schema.tables
3
Usuari admin creat a la BD
GET /auth/me retorna dades de l'usuari
4
Login funcional amb JWT
POST /auth/login retorna access_token
5
CRUD Municipis complet (7 endpoints)
Provar cada endpoint amb Postman/Thunder Client
6
CRUD Contactes complet (6 endpoints)
Provar cada endpoint amb Postman/Thunder Client
7
CRUD Deals complet (9 endpoints)
Provar cada endpoint amb Postman/Thunder Client
8
PATCH /deals/{id}/etapa funcional
Arrossegar targeta al Kanban canvia l'etapa a BD
9
Frontend: Login funcional
Login redirigeix a dashboard, logout torna al login
10
Frontend: Kanban amb drag & drop
Arrossegar targeta actualitza etapa en temps real
11
Frontend: Panell lateral deal
Clic a targeta obre drawer amb totes les seccions
12
Frontend: Notes humanes guardables
Escriure nota, guardar, recarregar: persisteix a BD
13
Frontend: Pàgina Municipis amb cerca
Cerca en temps real filtra resultats
14
Frontend: Pàgina Contactes
CRUD complet accessible des de la UI
15
Cap secret al codi font
Revisar que .env no estigui al repositori (.gitignore)
✅ FASE 1 COMPLETADA = Pots registrar municipis, contactes i deals, i gestionar el pipeline comercial B2G visualment. Estàs llest per iniciar la Fase 2: integració de correu CDmon i mòdul de pagaments.