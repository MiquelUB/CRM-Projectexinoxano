**FASE 2**

**Especificació Tècnica Completa**

*CRM Projecte Xino Xano*

Durada: Setmanes 3–4  |  Entorn: Local → VPS  |  Prerequisit: Fase 1 completada al 100%

Versió 1.0 — Març 2026

**OBJECTIU FASE 2: CRM complet per a ús diari real. En acabar: el correu de CDmon està integrat bidireccional (IN+OUT), els pagaments per transferència estan gestionats, i les alertes de renovació funcionen automàticament.**

# **1\. Resum dels Mòduls de Fase 2**

Fase 2 afegeix tres mòduls nous sobre la base de Fase 1, sense modificar el que ja funciona:

| Mòdul | Descripció | Prioritat |
| :---- | :---- | :---- |
| Integració Email IMAP/SMTP | Sync bidireccional CDmon. Emails IN+OUT vinculats a Deals. | CRÍTICA |
| Gestió de Pagaments | Registre de transferències bancàries. Estats i alertes. | ALTA |
| Alertes de Renovació | Alertes automàtiques per llicències que vencen en 30 dies. | ALTA |

# **2\. Mòdul 1 — Integració Email IMAP/SMTP**

**REGLA CRÍTICA: Sincronitzar SEMPRE les dues carpetes — INBOX (IN) i Sent/Enviats (OUT). Sense els emails sortints, l'agent IA veu la meitat de la conversa.**

## **2.1 Noves Taules de Base de Dades**

**Taula: emails**

| Camp | Tipus | Restriccions | Descripció |
| :---- | :---- | :---- | :---- |
| id | UUID | PK, DEFAULT gen\_random\_uuid() | Identificador únic |
| deal\_id | UUID | FK → deals.id, NULL permès | Deal associat (NULL \= pendent assignació manual) |
| contacte\_id | UUID | FK → contactes.id, NULL permès | Contacte associat |
| campanya\_id | UUID | FK → campanyes.id, NULL permès | Campanya associada (si és màrqueting) |
| from\_address | VARCHAR(255) | NOT NULL | Adreça remitent |
| to\_address | VARCHAR(255) | NOT NULL | Adreça destinatari |
| assumpte | VARCHAR(500) | NOT NULL | Assumpte de l'email |
| cos | TEXT |  | Cos complet (HTML o text pla) |
| direccio | VARCHAR(3) | NOT NULL, CHECK IN ('IN','OUT') | Direcció: IN (rebut) o OUT (enviat) |
| llegit | BOOLEAN | DEFAULT false | Si ha estat llegit al CRM |
| sincronitzat | BOOLEAN | DEFAULT false | True si ve d'IMAP, False si enviat des del CRM |
| message\_id\_extern | VARCHAR(500) | UNIQUE, NULL permès | Header Message-ID original (evita duplicats) |
| data\_email | TIMESTAMPTZ | NOT NULL | Data real de l'email (del header Date) |
| created\_at | TIMESTAMPTZ | DEFAULT NOW() | Data d'entrada al sistema |

**Taula: llicencies**

| Camp | Tipus | Restriccions | Descripció |
| :---- | :---- | :---- | :---- |
| id | UUID | PK, DEFAULT gen\_random\_uuid() | Identificador únic |
| deal\_id | UUID | FK → deals.id, NOT NULL, UNIQUE | Deal del qual deriva (1:1) |
| data\_inici | DATE | NOT NULL | Data d'inici de la llicència |
| data\_renovacio | DATE | NOT NULL | Data de venciment / renovació anual |
| estat | VARCHAR(50) | DEFAULT 'activa' | Valors: activa | suspesa | cancel·lada |
| notes | TEXT |  | Notes sobre la llicència |
| created\_at | TIMESTAMPTZ | DEFAULT NOW() | Data de creació |
| updated\_at | TIMESTAMPTZ | DEFAULT NOW() | Última modificació |

**Taula: pagaments**

| Camp | Tipus | Restriccions | Descripció |
| :---- | :---- | :---- | :---- |
| id | UUID | PK, DEFAULT gen\_random\_uuid() | Identificador únic |
| llicencia\_id | UUID | FK → llicencies.id, NOT NULL | Llicència associada |
| import | DECIMAL(10,2) | NOT NULL | Import en euros |
| tipus | VARCHAR(50) | NOT NULL | Valors: setup\_fee | llicencia\_anual |
| estat | VARCHAR(50) | DEFAULT 'emes' | Valors: emes | confirmat | vencut | proper |
| data\_emisio | DATE | NOT NULL | Data d'emissió de la factura |
| data\_limit | DATE |  | Data límit de pagament |
| data\_confirmacio | DATE |  | Data en què es confirma rebuda la transferència |
| notes | TEXT |  | Notes opcionals sobre el pagament |
| created\_at | TIMESTAMPTZ | DEFAULT NOW() | Data de creació |
| updated\_at | TIMESTAMPTZ | DEFAULT NOW() | Última modificació |

## **2.2 Sincronització IMAP — Lògica Completa**

El backend sincronitza cada 5 minuts via APScheduler. Procés obligatori:

1. Connectar a CDmon via IMAP SSL (port 993\)

2. Seleccionar INBOX → processar emails no vistos (UNSEEN) com a direccio='IN'

3. Seleccionar carpeta Sent/Enviats → processar emails nous com a direccio='OUT'

4. Per cada email: verificar si message\_id\_extern ja existeix a BD (evitar duplicats)

5. Executar algoritme de vinculació automàtica → assignar deal\_id si possible

6. Guardar a taula emails amb tots els camps

7. Si no es pot vincular automàticament → guardar amb deal\_id=NULL per assignació manual

## **2.3 Algoritme de Vinculació Email → Deal**

Prioritat descendent. S'aplica la primera regla que coincideix:

| Prioritat | Regla | Com funciona |
| :---- | :---- | :---- |
| 1a | Historial previ | Busca si l'adreça ja apareix en emails anteriors d'un deal actiu |
| 2a | Contacte directe | Busca contactes amb email exacte igual al remitent/destinatari |
| 3a | Domini municipal | Extreu el domini (@ajleida.cat) i busca municipis amb web similar |
| 4a | Manual | Cap coincidència: deal\_id=NULL, apareix a la safata pendent d'assignació |

## **2.4 Enviament SMTP des del CRM**

Quan l'usuari envia un email des del CRM, el sistema ha de:

* Enviar via SMTP CDmon (port 587, STARTTLS)

* Guardar immediatament a taula emails com a direccio='OUT', sincronitzat=True

* Vincular automàticament al deal des del qual s'envia

* NO esperar la pròxima sincronització IMAP per a emails enviats des del CRM

## **2.5 Nous Endpoints — /emails**

| Mètode | Endpoint | Params / Body | Resposta | Descripció |
| :---- | :---- | :---- | :---- | :---- |
| GET | /emails | ?deal\_id=\&direccio=\&llegit=\&page=1 | { items\[\], total, page } | Llista d'emails amb filtres |
| GET | /emails/{id} | — | Objecte email complet | Detall d'un email |
| POST | /emails/enviar | to, assumpte, cos, deal\_id | Objecte email creat | Envia email via SMTP |
| PATCH | /emails/{id}/deal | deal\_id | Objecte email actualitzat | Assignar email a deal manualment |
| PATCH | /emails/{id}/llegit | llegit: bool | Objecte email actualitzat | Marcar com a llegit/no llegit |
| POST | /emails/sync | — | { sincronitzats: int } | Forçar sincronització IMAP immediata |
| GET | /emails/pendents | — | Llista emails sense deal\_id | Emails no vinculats (assignació manual) |

## **2.6 Frontend — Mòdul d'Emails**

**Safata d'Entrada Integrada (/emails)**

* Llista d'emails ordenada per data\_email descendent (més recent primer)

* Filtre per: Tots / Rebuts (IN) / Enviats (OUT) / No llegits / Sense vincular

* Cada fila mostra: direccio (icona fletxa IN/OUT), remitent/destinatari, assumpte, deal vinculat (badge), data

* Clic a fila: obre el cos de l'email en panell lateral

* Botó 'Respondre': obre composer d'email pre-emplenat amb el fil

* Botó 'Vincular a Deal': selector de deal per als emails sense deal\_id

**Integració al Drawer del Deal (Fase 1\)**

* Afegir nova secció 'Fil d'Emails' al Drawer del Deal existent

* Mostra tots els emails IN i OUT del deal en ordre cronològic

* Visualització tipus 'bombolla de xat': IN a l'esquerra, OUT a la dreta

* Botó 'Nou Email' directament des del Drawer

**Safata de Pendents**

* Pàgina o secció per als emails amb deal\_id=NULL

* Permet assignar manualment cada email a un deal existent

* Comptador visible al sidebar (badge vermell si n'hi ha de pendents)

# **3\. Mòdul 2 — Gestió de Pagaments**

PXX cobra exclusivament per transferència bancària. El CRM gestiona l'estat de cada pagament manualment amb alertes automàtiques.

## **3.1 Estats de Pagament**

| Estat (BD) | Etiqueta Visual | Significat | Alerta Automàtica |
| :---- | :---- | :---- | :---- |
| emes | ⏳ Emès | Factura enviada, esperant transferència | Recordatori als 15 dies sense confirmar |
| confirmat | ✅ Confirmat | Transferència rebuda i verificada manualment | Cap |
| vencut | 🔴 Vençut | Data límit superada sense confirmar | Alerta urgent al dashboard |
| proper | 🔔 Proper | Renovació anual en els propers 30 dies | Avís preventiu al dashboard |

## **3.2 Flux de Creació de Pagament**

8. Deal passa a etapa 'tancat\_guanyat'

9. El sistema crea automàticament una Llicència associada al deal

10. L'usuari crea manualment els pagaments: Setup Fee \+ Llicència Anual

11. Quan rep la transferència: confirma el pagament manualment al CRM

12. El sistema calcula la data\_renovacio \= data\_confirmacio \+ 365 dies

13. 30 dies abans de data\_renovacio: alerta automàtica al dashboard

## **3.3 Nous Endpoints — /pagaments i /llicencies**

| Mètode | Endpoint | Body / Params | Resposta | Descripció |
| :---- | :---- | :---- | :---- | :---- |
| GET | /llicencies | ?estat=\&renovacio\_propera=30 | { items\[\], total } | Llista llicències amb filtre renovació |
| GET | /llicencies/{id} | — | Objecte llicència \+ pagaments | Detall complet amb historial pagaments |
| POST | /llicencies | deal\_id, data\_inici, data\_renovacio | Objecte llicència creada | Crear llicència per a deal tancat |
| PATCH | /llicencies/{id} | estat, data\_renovacio, notes | Objecte llicència actualitzat | Editar llicència |
| GET | /pagaments | ?llicencia\_id=\&estat=\&page=1 | { items\[\], total, resum{} } | Llista pagaments amb resum financer |
| POST | /pagaments | llicencia\_id, import, tipus, data\_emisio, data\_limit | Objecte pagament creat | Crear nou pagament |
| PATCH | /pagaments/{id}/confirmar | data\_confirmacio, notes | Objecte pagament actualitzat | Confirmar transferència rebuda |
| PATCH | /pagaments/{id} | estat, notes | Objecte pagament actualitzat | Editar estat o notes |
| GET | /pagaments/kpis | — | { arr\_total, pendent, vencut, proper\_30 } | KPIs financers globals |

## **3.4 Frontend — Mòdul de Pagaments**

**Pàgina /pagaments**

* Quatre blocs de KPIs a la part superior: ARR Total (€), Pendent de cobrar (€), Vençut (€), Renovacions en 30 dies (\#)

* Taula de pagaments amb filtre per estat (tots / emès / confirmat / vençut / proper)

* Cada fila: municipi, tipus pagament, import, estat (badge de color), data emissió, data límit, data confirmació

* Botó 'Confirmar' visible només en pagaments amb estat 'emes' o 'vencut'

* Botó 'Nou Pagament' per crear pagaments manualment

**Integració al Dashboard (ampliar Fase 1\)**

* Afegir al Bloc 2 del Dashboard: resum de pagaments vençuts i renovacions properes

* Badge d'alerta al sidebar si hi ha pagaments vençuts (punt vermell)

# **4\. Mòdul 3 — Alertes de Renovació**

Sistema d'alertes automàtiques per a llicències que vencen. Funciona amb un job en background que s'executa cada dia a les 08:00.

## **4.1 Lògica d'Alertes**

| Trigger | Condició | Acció del Sistema |
| :---- | :---- | :---- |
| 30 dies abans renovació | data\_renovacio \= TODAY \+ 30 dies | Crear pagament amb estat='proper' automàticament |
| 15 dies sense confirmar | estat='emes' i data\_emisio \< TODAY \- 15 | Canviar estat a 'vencut' \+ alerta dashboard |
| Data límit superada | data\_limit \< TODAY i estat\!='confirmat' | Canviar estat a 'vencut' \+ badge sidebar |

## **4.2 Endpoint d'Alertes**

| Mètode | Endpoint | Resposta | Descripció |
| :---- | :---- | :---- | :---- |
| GET | /alertes | { renovacions\[\], pagaments\_vençuts\[\], emails\_pendents\[\] } | Totes les alertes actives agrupades per tipus |
| GET | /alertes/count | { total, renovacions, vençuts, emails\_pendents } | Comptadors per al badge del sidebar |

# **5\. Scheduler — APScheduler**

Dos jobs en background integrats al backend FastAPI:

| Job | Freqüència | Funció | Descripció |
| :---- | :---- | :---- | :---- |
| sync\_emails | Cada 5 minuts | sync\_imap\_inbox() \+ sync\_imap\_sent() | Sincronitza INBOX i Sent de CDmon |
| check\_alertes | Cada dia 08:00 | update\_pagaments\_vençuts() \+ crear\_renovacions\_properes() | Actualitza estats de pagaments i crea alertes |

\# Instal·lació addicional necessària

pip install apscheduler

# **6\. Variables d'Entorn Noves (.env)**

Afegir al fitxer .env existent de Fase 1:

\# Correu CDmon — IMAP (recepció)

IMAP\_HOST=mail.cdmon.com

IMAP\_PORT=993

IMAP\_USER=crm@projectexinoxano.cat

IMAP\_PASSWORD=contrasenya\_segura

IMAP\_SSL=true

\# Correu CDmon — SMTP (enviament)

SMTP\_HOST=mail.cdmon.com

SMTP\_PORT=587

SMTP\_USER=crm@projectexinoxano.cat

SMTP\_PASSWORD=contrasenya\_segura

SMTP\_TLS=true

# **7\. Task Group Suggerit per a Antigravity**

**Entregar aquest Task Group a Antigravity per iniciar la Fase 2\. Segueix l'ordre de subtasques — BD primer, sempre.**

TASK GROUP: Fase 2 — Email \+ Pagaments \+ Alertes

Objectiu: CRM complet per a ús diari real amb correu integrat i gestió financera

Subtasca 1 — Base de Dades \[PRIMER\]

  → Migració Alembic: taules emails, llicencies, pagaments

  → Índexs: emails(deal\_id), emails(message\_id\_extern), llicencies(deal\_id),

           llicencies(data\_renovacio), pagaments(llicencia\_id), pagaments(estat)

  → Trigger updated\_at per a llicencies i pagaments

Subtasca 2 — Backend Email \[depèn de Subtasca 1\]

  → backend/services/email\_sync.py: sync INBOX \+ Sent (IN i OUT obligatori)

  → backend/services/email\_sender.py: enviament SMTP

  → backend/routers/emails.py: 7 endpoints

  → Integrar APScheduler a main.py: job sync cada 5 minuts

Subtasca 3 — Backend Pagaments \[en paral·lel amb Subtasca 2\]

  → backend/routers/llicencies.py: 4 endpoints

  → backend/routers/pagaments.py: 5 endpoints \+ /kpis

  → backend/routers/alertes.py: 2 endpoints

  → Integrar APScheduler: job check\_alertes cada dia 08:00

Subtasca 4 — Frontend Email \[depèn de Subtasca 2\]

  → frontend/app/emails/page.tsx: safata d'entrada integrada

  → Ampliar Drawer del Deal: afegir secció 'Fil d'Emails' (bombolla IN/OUT)

  → frontend/app/emails/pendents: emails sense vincular

  → Badge al sidebar per emails pendents d'assignar

Subtasca 5 — Frontend Pagaments \[en paral·lel amb Subtasca 4\]

  → frontend/app/pagaments/page.tsx: taula \+ KPIs financers

  → Ampliar Dashboard: bloc alertes renovació \+ pagaments vençuts

  → Badge al sidebar per pagaments vençuts

Subtasca 6 — Verificació i Report \[sempre al final\]

  → Verificar sync IMAP: emails IN i OUT apareixen al CRM

  → Verificar enviament SMTP: email enviat des del CRM arriba al destinatari

  → Verificar pagament: crear, confirmar, veure canvi d'estat

  → Verificar alerta: llicència pròxima apareix al dashboard

  → Crear REPORT\_YYYYMMDD\_fase2\_completada.md

  → Actualitzar REPORTS\_INDEX.md

# **8\. Checklist de Finalització Fase 2**

15 punts obligatoris abans de declarar Fase 2 completada:

| \# | Ítem | Verificació |
| :---- | :---- | :---- |
| 1 | Migració BD: taules emails, llicencies, pagaments creades | SELECT table\_name FROM information\_schema.tables WHERE table\_name IN ('emails','llicencies','pagaments') |
| 2 | Índexs creats per a totes les FK i camps de filtre | SELECT indexname FROM pg\_indexes WHERE tablename IN ('emails','pagaments','llicencies') |
| 3 | Sync IMAP INBOX funcional: emails rebuts apareixen al CRM | Enviar email de prova a crm@projectexinoxano.cat i verificar que apareix |
| 4 | Sync IMAP Sent funcional: emails enviats via Thunderbird apareixen com OUT | Enviar email des de Thunderbird i verificar que apareix com a direccio='OUT' |
| 5 | Enviament SMTP des del CRM funcional | Enviar email des del CRM i verificar recepció al destinatari |
| 6 | Algoritme de vinculació: emails s'assignen automàticament als deals | Enviar email amb adreça ja vinculada i verificar que apareix al deal correcte |
| 7 | Emails pendents (deal\_id=NULL) apareixen a la safata de pendents | Enviar email desconegut i verificar que apareix com a pendent |
| 8 | Fil d'emails al Drawer del Deal: mostra IN i OUT en ordre cronològic | Obrir un deal i verificar que el fil d'emails és complet i bidireccional |
| 9 | CRUD Llicències funcional (4 endpoints) | Crear llicència per a deal tancat\_guanyat |
| 10 | CRUD Pagaments funcional (5 endpoints \+ /kpis) | Crear pagament, confirmar-lo, verificar canvi d'estat |
| 11 | KPIs financers al dashboard i /pagaments: ARR, pendent, vençut | Verificar que els imports calculats coincideixen amb els pagaments existents |
| 12 | Alerta renovació: llicència en 30 dies apareix al dashboard | Crear llicència amb data\_renovacio \= avui \+ 25 dies i verificar alerta |
| 13 | Badge sidebar: pagaments vençuts i emails pendents mostren comptador | Crear pagament vençut i verificar que apareix el badge al sidebar |
| 14 | Scheduler APScheduler actiu: jobs s'executen sense errors als logs | Revisar logs del backend i confirmar que els jobs s'executen |
| 15 | REPORT\_fase2\_completada.md creat i REPORTS\_INDEX.md actualitzat | Verificar existència dels fitxers a .agents/reports/ |

**✅ FASE 2 COMPLETADA \= El CRM és una eina de treball real. Correu integrat bidireccional, pagaments controlats i alertes automàtiques. Llest per iniciar Fase 3: Campanyes Email \+ Agent IA (OpenRouter).**