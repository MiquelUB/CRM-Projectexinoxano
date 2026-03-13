**FASE 3**

**Agent IA \+ Estadístiques d'Email**

*CRM Projecte Xino Xano*

Durada: Setmanes 5–6  |  Prerequisit: Fase 2 completada  |  Requereix: OpenRouter API Key

Versió 1.0 — Març 2026

**OBJECTIU FASE 3: El CRM del 1%. L'agent IA llegeix el context complet de cada deal (emails IN+OUT \+ notes humanes) i proposa accions concretes per tancar. Les estadístiques d'email revelen quins leads estan realment interessats.**

# **1\. Resum dels Mòduls de Fase 3**

| Mòdul | Descripció | Prioritat |
| :---- | :---- | :---- |
| Agent IA — Redacció Emails | Redacta emails de seguiment B2G basant-se en el fil complet del deal. | CRÍTICA |
| Agent IA — Anàlisi de Deal | Analitza per què un lead no avança i proposa el proper pas. | CRÍTICA |
| Agent IA — Resum Executiu | Genera un resum executiu de l'estat actual d'un deal. | ALTA |
| Estadístiques d'Obertura | Tracking pixel per saber si l'ajuntament ha obert els emails enviats. | ALTA |

**REGLA ABSOLUTA: Mai OpenAI. Sempre OpenRouter. URL base: https://openrouter.ai/api/v1. El model es passa com a paràmetre — mai hard-coded.**

# **2\. Arquitectura de l'Agent IA**

L'agent no substitueix el comercial: l'assisteix. Rep el context complet del deal i proposa, però la decisió final sempre és humana.

## **2.1 Context que rep l'Agent**

Per cada crida a l'agent, el backend construeix un context complet amb:

* Dades del deal: títol, etapa actual, pla (ROURE/MIRADOR/TERRITORI), valor, dies en etapa, proper pas acordat.

* Dades del municipi: nom, tipus (ajuntament/diputació), província, població.

* Dades del contacte: nom, càrrec.

* Notes humanes: tot el text lliure escrit pel comercial sobre converses telefòniques i reunions.

* Fil complet d'emails IN i OUT: ordenats cronològicament, amb remitent, data i cos (màx. 500 caràcters per email).

* Historial d'etapes: quan va canviar d'etapa i quants dies ha estat a cada una.

## **2.2 Selecció de Model per Tasca**

| Tasca | Model Recomanat | Justificació |
| :---- | :---- | :---- |
| Redacció email seguiment B2G | anthropic/claude-3.5-sonnet | Millor català formal i comprensió de context llarg |
| Anàlisi per què no avança | anthropic/claude-3.5-sonnet | Raonament complex sobre dinàmiques B2G |
| Resum executiu deal | mistralai/mistral-small-3.1-24b-instruct | Ràpid i econòmic per resums estructurats |

El model es pot canviar en temps d'execució des del frontend sense modificar codi.

# **3\. Mòdul 1 — Redacció d'Emails de Seguiment**

## **3.1 Funcionament**

Des del Drawer del Deal, el comercial pot demanar a l'agent que redacti un email de seguiment. L'agent llegeix tot el fil i genera un email professional en català adaptat al context específic del deal.

## **3.2 Nou Endpoint — POST /agent/redactar-email**

| Camp | Tipus | Descripció |
| :---- | :---- | :---- |
| deal\_id | UUID | Deal per al qual es redacta l'email |
| instruccions | string | Indicacions específiques del comercial (ex: 'insistir en el preu', 'demanar reunió') |
| model | string | Model OpenRouter a usar. Default: anthropic/claude-3.5-sonnet |
| to\_address | string | Adreça destinatari (pre-emplenat amb el contacte del deal) |

**Resposta:**

{ "assumpte": "Seguiment proposta PXX — Ajuntament de Lleida",

  "cos\_html": "\<p\>Benvolgut Sr. ...\</p\>",

  "model\_usat": "anthropic/claude-3.5-sonnet",

  "tokens\_usats": 1247 }

## **3.3 System Prompt — Redacció Email**

Ets un expert en comunicació B2G amb administracions públiques catalanes.

Redactes emails professionals, formals però propers, en català correcte i sense tecnicismes.

L'objectiu sempre és avançar el deal cap al tancament.

Format: assumpte clar \+ cos amb salutació formal, cos breu i orientat a l'acció, comiat professional.

Mai menciones que ets una IA. Escrius en nom del comercial de PXX.

## **3.4 Frontend — Composer d'Email amb IA**

* Botó 'Redactar amb IA' al Drawer del Deal, secció Fil d'Emails.

* Modal amb: camp d'instruccions (textarea), selector de model, botó 'Generar'.

* Mentre genera: skeleton loading \+ missatge 'L'agent està llegint el fil del deal...'

* Resultat: assumpte i cos pre-emplenat al composer d'email existent.

* El comercial pot editar lliurement abans d'enviar — l'IA proposa, l'humà decideix.

* Botó 'Regenerar' per obtenir una versió alternativa sense tancar el modal.

# **4\. Mòdul 2 — Anàlisi de Deal (Per què no avança?)**

## **4.1 Funcionament**

Des del Drawer del Deal, el comercial pot demanar a l'agent una anàlisi de per què el deal està estancat i quina és la millor acció per desbloquejar-lo.

## **4.2 Nou Endpoint — POST /agent/analitzar-deal**

| Camp | Tipus | Descripció |
| :---- | :---- | :---- |
| deal\_id | UUID | Deal a analitzar |
| model | string | Model OpenRouter. Default: anthropic/claude-3.5-sonnet |

**Resposta estructurada (JSON):**

{ "obstacle\_principal": "El contacte no té poder de decisió real.",

  "proper\_pas\_recomanat": "Sol·licitar reunió amb l'alcalde directament.",

  "missatge\_clau": "Emfatitzar l'estalvi vs app a mida: 23.500€ vs 80.000€.",

  "urgencia": "alta",

  "model\_usat": "anthropic/claude-3.5-sonnet" }

## **4.3 System Prompt — Anàlisi de Deal**

Ets un assessor comercial expert en vendes B2G a administracions públiques espanyoles.

Analitzes el context complet d'un deal i identifies els obstacles reals per tancar-lo.

Respons SEMPRE en format JSON vàlid amb els camps: obstacle\_principal,

proper\_pas\_recomanat, missatge\_clau, urgencia (baixa/mitjana/alta).

Sigues directe i accionable. Cap teoria genèrica — respostes específiques al context donat.

Respon sempre en català.

## **4.4 Frontend — Panell d'Anàlisi**

* Botó 'Analitzar Deal' al Drawer, secció Notes Humanes.

* Resultat en targeta visual amb 3 seccions: Obstacle Principal (vermell), Proper Pas Recomanat (verd), Missatge Clau (blau).

* Botó 'Aplicar com a Proper Pas' — omplena automàticament el camp proper\_pas del deal.

* Indicador d'urgència: badge Alt/Mitjà/Baix al costat del títol del deal al Kanban.

# **5\. Mòdul 3 — Resum Executiu del Deal**

## **5.1 Funcionament**

Genera un resum executiu breu de l'estat actual del deal. Útil per preparar una reunió o refrescar el context després d'un període d'inactivitat.

## **5.2 Nou Endpoint — POST /agent/resum-deal**

| Camp | Tipus | Descripció |
| :---- | :---- | :---- |
| deal\_id | UUID | Deal a resumir |
| model | string | Model OpenRouter. Default: mistralai/mistral-small-3.1-24b-instruct |

**Resposta:**

{ "resum": "Deal amb l'Ajuntament de Lleida (pla MIRADOR, 10.500€). Contacte: 

  Joan Puig, Tècnic de Turisme. En etapa Proposta Enviada des de fa 12 dies. 

  Darrera interacció: email del client demanant info sobre suport tècnic. 

  Proper pas: enviar document de SLA i casos d'èxit similars.",

  "model\_usat": "mistralai/mistral-small-3.1-24b-instruct" }

## **5.3 Frontend**

* Botó 'Resum IA' a la capçalera del Drawer del Deal.

* Resultat en modal o tooltip expandible — màx. 5 línies de text.

* S'actualitza automàticament si hi ha canvis al deal des de l'últim resum.

# **6\. Mòdul 4 — Estadístiques d'Obertura d'Emails**

## **6.1 Com funciona el Tracking Pixel**

Quan el CRM envia un email via SMTP, insereix un píxel transparent 1x1px al cos HTML de l'email. Quan el destinatari obre l'email, el seu client de correu carrega el píxel i el nostre servidor registra l'obertura.

## **6.2 Modificació de Taula emails**

| Camp Nou | Tipus | Descripció |
| :---- | :---- | :---- |
| tracking\_token | VARCHAR(100) | Token únic per email. Format: UUID sense guions. |
| obert | BOOLEAN | DEFAULT false. True quan el píxel es carrega. |
| data\_obertura | TIMESTAMPTZ | Data i hora de la primera obertura. |
| nombre\_obertures | INTEGER | DEFAULT 0\. Comptador d'obertures totals. |
| ip\_obertura | VARCHAR(50) | IP des de la qual s'ha obert (referència). |

## **6.3 Nou Endpoint — GET /tracking/{token}**

Endpoint públic (sense autenticació) que retorna el píxel i registra l'obertura:

1. Rep la petició GET amb el token únic.

2. Busca l'email a BD per tracking\_token.

3. Actualitza: obert=true, data\_obertura=NOW(), nombre\_obertures+=1, ip\_obertura.

4. Retorna una imatge PNG transparent 1x1px (Content-Type: image/png).

**IMPORTANT: El tracking pixel s'insereix NOMÉS als emails enviats des del CRM (direccio='OUT'). Mai als emails sincronitzats via IMAP.**

## **6.4 Inserció del Pixel a l'Email**

\# A email\_sender.py, abans d'enviar:

tracking\_token \= str(uuid.uuid4()).replace('-', '')

pixel\_url \= f'{BASE\_URL}/tracking/{tracking\_token}'

pixel\_html \= f'\<img src="{pixel\_url}" width="1" height="1" /\>'

cos\_html\_final \= cos\_html \+ pixel\_html

## **6.5 Frontend — Estadístiques**

* Icona d'ull al costat de cada email enviat: gris=no obert, verd=obert.

* Tooltip en hover: 'Obert X vegades. Primera obertura: DD/MM/YYYY HH:MM'

* Al Drawer del Deal: indicador visual si l'últim email enviat ha estat obert.

* Al Dashboard: nou KPI 'Taxa d'obertura emails' (% emails oberts / enviats últims 30 dies).

# **7\. Nou Router — backend/routers/agent.py**

| Mètode | Endpoint | Body | Resposta | Descripció |
| :---- | :---- | :---- | :---- | :---- |
| POST | /agent/redactar-email | deal\_id, instruccions, model, to\_address | { assumpte, cos\_html, model\_usat, tokens\_usats } | Redacta email de seguiment |
| POST | /agent/analitzar-deal | deal\_id, model | { obstacle\_principal, proper\_pas\_recomanat, missatge\_clau, urgencia } | Analitza obstacles del deal |
| POST | /agent/resum-deal | deal\_id, model | { resum, model\_usat } | Resum executiu breu |
| GET | /tracking/{token} | — | Imatge PNG 1x1px | Registra obertura email (públic) |

# **8\. Variables d'Entorn Noves (.env)**

\# OpenRouter

OPENROUTER\_API\_KEY=sk-or-v1-...

OPENROUTER\_BASE\_URL=https://openrouter.ai/api/v1

\# Tracking pixel — URL pública del servidor

BASE\_URL=http://localhost:8000   \# Canviar per URL VPS en producció

# **9\. Task Group per a Antigravity**

**Entregar aquest Task Group a Antigravity per iniciar la Fase 3\.**

TASK GROUP: Fase 3 — Agent IA \+ Estadístiques Obertura Emails

Objectiu: CRM del 1% — IA que llegeix el context complet i proposa accions de tancament

Subtasca 1 — Base de Dades \[PRIMER\]

  → Migració Alembic: afegir camps tracking\_token, obert, data\_obertura,

    nombre\_obertures, ip\_obertura a taula emails

  → Índex: emails(tracking\_token) — consultat en cada obertura

Subtasca 2 — Backend Agent IA \[depèn de Subtasca 1\]

  → backend/services/openrouter\_client.py: client base reutilitzable

  → backend/services/agent\_service.py: lògica de construcció de context

    (llegir deal \+ emails IN/OUT \+ notes \+ historial etapes)

  → backend/routers/agent.py: 3 endpoints POST \+ 1 GET tracking

  → Afegir OPENROUTER\_API\_KEY i BASE\_URL al .env

Subtasca 3 — Backend Tracking \[en paral·lel amb Subtasca 2\]

  → Modificar email\_sender.py: generar tracking\_token i inserir pixel HTML

  → Endpoint GET /tracking/{token}: retorna PNG 1x1 i registra obertura

Subtasca 4 — Frontend Agent IA \[depèn de Subtasca 2\]

  → Drawer Deal: botó 'Redactar amb IA' → modal composer amb instruccions

  → Drawer Deal: botó 'Analitzar Deal' → targeta obstacle/proper pas/missatge

  → Drawer Deal: botó 'Resum IA' → modal resum executiu

  → Selector de model visible per l'usuari (desplegable)

Subtasca 5 — Frontend Tracking \[en paral·lel amb Subtasca 4\]

  → Icona d'ull als emails enviats (gris/verd segons estat obert)

  → Tooltip amb data i nombre d'obertures

  → Dashboard: nou KPI taxa d'obertura últims 30 dies

Subtasca 6 — Verificació i Report \[sempre al final\]

  → Test redacció email: verificar que l'agent genera email en català formal

  → Test anàlisi: verificar que retorna JSON estructurat correctament

  → Test tracking: enviar email, obrir-lo, verificar que obert=true a BD

  → Verificar que MAI s'usa OpenAI (revisar tots els imports)

  → Crear REPORT\_YYYYMMDD\_fase3\_completada.md

  → Actualitzar REPORTS\_INDEX.md

# **10\. Checklist de Finalització Fase 3**

| \# | Ítem | Verificació |
| :---- | :---- | :---- |
| 1 | Migració BD: camps tracking a taula emails | SELECT column\_name FROM information\_schema.columns WHERE table\_name='emails' |
| 2 | OPENROUTER\_API\_KEY al .env (mai al codi) | grep \-r 'sk-or' backend/ (no ha de trobar res) |
| 3 | Client OpenRouter usa URL https://openrouter.ai/api/v1 | Revisar openrouter\_client.py |
| 4 | Cap import d'openai al codi | grep \-r 'import openai' backend/ (ha de ser buit) |
| 5 | Endpoint redactar-email retorna assumpte \+ cos en català | POST /agent/redactar-email amb deal real |
| 6 | Endpoint analitzar-deal retorna JSON estructurat | Verificar camps: obstacle\_principal, proper\_pas\_recomanat, missatge\_clau, urgencia |
| 7 | Endpoint resum-deal retorna resum breu (\<5 línies) | POST /agent/resum-deal amb deal actiu |
| 8 | Tracking pixel inserit als emails enviats des del CRM | Enviar email i inspeccionar HTML — ha de contenir \<img src=.../tracking/...\> |
| 9 | Endpoint GET /tracking/{token} retorna PNG i registra obertura | Cridar URL del pixel i verificar obert=true a BD |
| 10 | Icona d'ull al frontend mostra estat obertura correctament | Verificar visualment emails enviats |
| 11 | Botó 'Redactar amb IA' funcional al Drawer del Deal | Generar email i verificar que es pot editar i enviar |
| 12 | Botó 'Analitzar Deal' mostra targeta amb 3 seccions | Verificar visualment el resultat de l'anàlisi |
| 13 | Botó 'Resum IA' mostra resum en modal | Verificar contingut del resum per a un deal amb historial |
| 14 | Selector de model visible i funcional al frontend | Canviar model i verificar que s'usa el seleccionat |
| 15 | REPORT\_fase3\_completada.md creat i REPORTS\_INDEX.md actualitzat | Verificar existència a .agents/reports/ |

**✅ FASE 3 COMPLETADA \= CRM del 1%. L'agent IA llegeix el context complet de cada deal i proposa accions concretes. El comercial sap si els ajuntaments han obert els emails. PXX té ara l'eina comercial més avançada del sector.**