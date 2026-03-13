# Report Complet Fase 2 - CRM PXX

Aquest document resumeix els treballs duts a terme per a donar per finalitzada de manera íntegra la Fase 2 del CRM PXX (Mòdul d'Emails i Mòdul Llicències i Pagaments).

## Resum d'Actuacions

### 1. Backend (Estructura, API i Base de Dades)
- S'han creat amb **Alembic** les noves taules de la Fase 2 (`emails`, `llicencies`, a més de `pagaments`). S'ha netejat i unificat la base de dades local mitjançant la reconfiguració de PostgreSQL cap al port `5433` (assequible per port mapper de Docker evitant conflictes en local).
- S'han creat dos arxius al directori de serveis: `backend/services/email_sync.py` (per connectar per IMAP al servidor de CDmon, syncronitzant "INBOX" i sent items i assignant automàticament els correus als deals mitjançant 3 regles en ordre de prelació); i `backend/services/email_sender.py` per enviar sota SMTP correus natius de la plataforma.
- S'han creat tres nous end-points tipus Router a `routers/` per cobrir CRUD de `Llicencies`, `Pagaments` (amb endpoint especific per a confirmació) i `Alertes`.
- S'ha habilitat la planificació en back-ground mitjançant instància `apscheduler` dintre de `backend/main.py`. El servei farà queries globals d'emails cada 5 minuts i cada dia a les 08.00 hores afegirà alertes de renovació i processará la vigència dels pagaments emesos envers els 15 dies naturals.

### 2. Frontend (Interfície)
- **Mòdul InBox General (`/emails`)**: Mostra una taula dinàmica i reactiva dels correus entrants (IN) i sortints (OUT), si estan llegits o no, acompanyats de botons de filtre "ALL", "IN", "OUT", "UNREAD". Disposa d'un botó per arrancar la sincro IMAP sota demanda.
- **Mòdul Mòdul Pendents (`/emails/pendents`)**: Vista detallada sobre tots aquells correus l'algoritme dels quals no hagi sigut capaç d'apairar amb cap DEAL actiu. Permet vincular-los manualment des d'un desplegable seleccionador simple ad-hoc.
- **Detall del Kanban (Deal Drawer)**: Reprogramació per afegir un widget complet sota el deal a tall de feed cronològic de correus. També s'habilitat exclusivament quan el deal es mou a 'Tancat_Guanyat' la presència del gestor manual de Llicència, capaç de crear i previsualitzar informació essencial.
- **Tauler de Pagaments (`/pagaments`)**: Renderització de la base de capex i billing; una taula filtrable dels elements, juntament a l'esment explícit als 4 KPIs superios: (ARR Total, Pendent, Vencut i Renovacions próximes). Els items no confirmats tenen un pushable de "Confirmar".
- **Dashboard (`/dashboard`)**: Enganxades els models d'alertes i pendents a la previsualització inicial del bloc base que abans estavan per omplir com a placeholders.

S'ha validat el correcte funcionament amb el backend FastApi Aixecat amb uvicorn així com la injecció dels components Frontend en funcionament reactiu i integrat.

## Següents Passos:
Passem ara a mans de l'usuari la certificació humana. Fes review del sistema si així ho desitges mitjançant la plataforma o accepta l'estat per poder començar a planificar o executar els apartats de la Fase 3, referents majoritariament a Inteligència Artificial.
