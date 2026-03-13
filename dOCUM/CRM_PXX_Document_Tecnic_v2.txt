CRM
PROJECTE XINO XANO
Document Tècnic Definitiu — v1.0
Estat: APROVAT ✅
Data: Març 2026
Arquitecte: CRM Sènior Consultor
1. Visió General i Objectius
El CRM de Projecte Xino Xano (PXX) és una aplicació web a mida dissenyada exclusivament per gestionar el cicle de vida comercial B2G (Business to Government). No és un CRM genèric adaptat: és una eina construïda des de zero per al cas d'ús específic de vendre llicències SaaS a Diputacions i Ajuntaments.
Objectius Primaris
Gestionar el pipeline comercial B2G des del lead fins al contracte signat.
Controlar l'estat de llicències, renovacions anuals i pagaments per transferència.
Centralitzar tota la comunicació per email (CDmon/Thunderbird) vinculada a cada deal.
Executar campanyes d'email màrqueting híbrides per convertir leads en clients.
Donar suport a la presa de decisions comercials mitjançant un agent IA (OpenRouter).
Gestionar tasques internes de desenvolupament i roadmap del producte PXX.
Principi Rector: Sobirania Total
El CRM s'allotja al VPS propi de PXX. Cap dada surt del servidor de l'empresa. Això és coherent amb la proposta de valor de Sobirania Digital que PXX ven als seus clients.
2. Stack Tecnològic — El Veredicte Final
Cada decisió tecnològica respon a 3 criteris: coherència amb PXX Studio, capacitat d'integració IA nativa i velocitat de desenvolupament màxima.
Capa
Tecnologia
Justificació
Frontend
Next.js 14 + TypeScript
Coherent amb PXX Studio. SSR + rendiment òptim.
Estils UI
Tailwind CSS + shadcn/ui
Components professionals sense disseny des de zero.
Backend / API
FastAPI (Python)
IA nativa, async, rendiment alt, ecosistema ML/AI.
Base de Dades
PostgreSQL + PostGIS
Ja conegut de PXX. Espacial, robust, gratuït.
IA
OpenRouter (model TBD)
Multi-model. Tries el millor per cada tasca.
Correu
IMAP/SMTP via imaplib (Python)
Integració directa amb CDmon sense intermediaris.
Infraestructura
VPS propi + Docker Compose
Sobirania total. 0€ en llicències externes.
Autenticació
JWT + Refresh Tokens
Seguretat estàndard B2G. Compliment GDPR.
Reverse Proxy
Nginx + HTTPS forçat
Seguretat, rendiment i domini personalitzat.
3. Model de Dades — Les 8 Entitats Clau
L'estructura de dades reflecteix exactament el flux de treball comercial B2G de PXX:
3.1 Entitats Principals
Entitat (Taula)
Camps Clau
Relació
MUNICIPIS
id, nom, provincia, poblacio, tipus (ajunt/diput), web, notes
1:N amb Contactes i Deals
CONTACTES
id, nom, carrec, email, telefon, municipi_id, notes_humanes
N:1 Municipi, 1:N Deals
DEALS
id, titol, etapa, valor_setup, valor_llicencia, data_creacio, data_tancament
N:1 Municipi, N:1 Contacte
LLICÈNCIES
id, deal_id, data_inici, data_renovacio, estat (activa/pendent/vençuda)
1:1 Deal
PAGAMENTS
id, llicencia_id, import, tipus (setup/anual), estat, data_transferencia, notes
N:1 Llicència
EMAILS
id, deal_id, contacte_id, assumpte, cos, data, direccio (IN/OUT), campanya_id
N:1 Deal
CAMPANYES
id, nom, sequencia_emails (JSON), estat, data_inici, estadistiques (JSON)
1:N Emails
TASQUES
id, titol, tipus (comercial/dev), assignat_a, deal_id, data_limit, estat, notes
N:1 Deal (opcional)
3.2 Flux de Relacions
MUNICIPIS  ──►  CONTACTES  ──►  DEALS  ──►  LLICÈNCIES  ──►  PAGAMENTS
                                    │                    │
                                    ▼                    ▼
                                 EMAILS              TASQUES
                                    │
                                    ▼
                                CAMPANYES
4. Dashboard — Els 5 Blocs Visuals
El dashboard respon 5 preguntes estratègiques en menys de 3 segons. Disseny sobri, professional i orientat a l'eficiència comercial B2G.
Bloc 1 — Pipeline Comercial Visual
Kanban horitzontal amb 6 etapes. Cada targeta mostra: nom del municipi, valor del deal i dies en l'etapa actual.
Etapa
Descripció
Acció Clau
🔵 Prospecte
Lead identificat, sense contacte
Afegir a campanya email
📧 Contacte Inicial
Primer email enviat / resposta rebuda
Registrar nota humana
📊 Demo Feta
Presentació realitzada
Enviar proposta formal
📄 Proposta Enviada
Document enviat, pendent resposta
Seguiment a 7 dies
⚙️ Tramitació Admin
Aprovació interna de l'ajuntament
Esperar + contacte polític
✅ Tancat Guanyat
Contracte signat, activar llicència
Crear llicència + factura
Bloc 2 — Estat de Llicències i Pagaments
Panell de control financer en temps real. Quatre estats visuals amb color:
✅ PAGAT — clients actius amb llicència vigent i pagament confirmat.
⏳ PENDENT — setup fee o renovació enviada, esperant transferència.
🔴 VENÇUT — llicència caducada sense renovació. Risc de churn.
🔔 RENOVACIÓ PRÒXIMA — llicències que vencen en els propers 30 dies.
KPIs visibles sempre al dashboard: ARR Total (€), MRR Mensualitzat (€), Clients Actius (#), Import Pendent de Cobrar (€).
Bloc 3 — Safata d'Entrada Integrada
Els emails de CDmon sincronitzats via IMAP es mostren vinculats al seu Deal/Contacte. Des d'aquí es pot respondre directament sense sortir del CRM. El sistema vincula automàticament l'email al deal corresponent per domini o adreça.
Bloc 4 — Activitat Recent i Tasques Pendents
Feed cronològic de les últimes accions: emails enviats/rebuts, notes afegides, etapes canviades, pagaments registrats. Llista de tasques urgents del dia amb accés directe al deal relacionat.
Bloc 5 — Assistent IA (OpenRouter)
Panell lateral accessible des de qualsevol deal. L'agent rep com a context: tots els emails del fil, totes les notes humanes escrites i l'etapa actual del deal. Pot suggerir el proper pas comercial, redactar un email de seguiment o analitzar per què un lead no avança.
5. Mòdul d'Email — Tres Capes
5.1 Integració IMAP/SMTP (CDmon) — Fils Complets IN + OUT
L'agent IA necessita veure TOTA la conversa: tant el que ha dit el client com el que hem respost nosaltres. Per això el sistema sincronitza obligatòriament les dues carpetes de CDmon:
Carpeta IMAP
Tipus
Camp direccio
Descripció
INBOX
Rebuts
IN
Emails que arriben del client/ajuntament
Sent / Enviats
Enviats des de Thunderbird
OUT
Emails enviats manualment fora del CRM
Carpeta CRM-Sent
Enviats des del CRM
OUT
Emails enviats directament des del CRM
Sincronització cada 5 minuts. Procés complet:
Lectura d'INBOX i carpeta Enviats via imaplib (Python).
Parser identifica a quin Deal pertany per domini del remitent/destinatari o historial previ.
Tots els emails guardats a taula EMAILS amb camp direccio (IN/OUT) i timestamp real.
Enviament sortint via SMTP des del CRM guardat automàticament com a OUT.
Resultat: l'agent IA rep el fil cronològic complet i real de cada conversa.
5.2 Notes Humanes per Deal
Cada Deal té un camp de text lliure per registrar tot el que passa fora del correu electrònic: trucades telefòniques, reunions presencials, comentaris informals, acords verbals. No hi ha etiquetes ni puntuacions. El text lliure preserva el context i el matisos humans de cada conversa.
Les notes poden fer referència a emails anteriors o a altres converses del historial. Quan es consulta l'agent IA, rep tot aquest context acumulat per oferir un suggeriment de tancament personalitzat.
5.3 Campanyes d'Email Màrqueting Híbrides
Funnel de conversió predefinit per convertir leads (Ajuntaments/Diputacions) en clients. Funcionament híbrid: la seqüència s'executa automàticament però el comercial pot intervenir en qualsevol moment.
Pas
Email
Timing
Intervenció Humana Possible
1
Introducció PXX + proposta de valor sobirania digital
Dia 0 (manual)
Personalitzar nom/municipi
2
Cas d'èxit: exemple Diputació Provincial
Dia 7 (automàtic)
Pausar si hi ha resposta
3
Calculadora ROI: cost vs. app a mida
Dia 14 (automàtic)
Substituir per email personal
4
Demo gratuïta: oferta limitada
Dia 21 (automàtic)
Ajustar data/hora demo
5
Seguiment post-silenci
Dia 30 (automàtic)
Escriure missatge manual
Estadístiques per Campanya
Emails enviats / rebuts / obertes (tracking pixel).
Taxa de resposta per pas de la seqüència.
Conversions: leads que han avançat d'etapa al pipeline.
Leads freds: no han obert cap email en 30+ dies.
6. Mòdul de Pagaments (Transferència Bancària)
PXX no utilitza passarel·les de pagament. Tots els cobraments es fan per transferència bancària. El CRM gestiona l'estat de cada pagament manualment però amb alertes automàtiques.
Estat
Definició
Alerta Automàtica
⏳ Emès
Factura enviada al client, esperant transferència
Recordatori als 15 dies
✅ Confirmat
Transferència rebuda i verificada manualment
Cap
🔴 Vençut
Factura sense pagar passada la data límit
Alerta urgent al dashboard
📅 Pròxim
Renovació anual en els propers 30 dies
Avís preventiu
Cada pagament registra: import, tipus (Setup Fee / Llicència Anual), data prevista, data de recepció confirmada i notes opcionals. El comercial confirma el pagament manualment un cop verifica l'extracte bancari.
7. Agent IA — OpenRouter
L'IA no substitueix el comercial: l'assisteix. La clau humana és irrenunciable en B2G; l'IA processa el context i proposa, però decideix la persona.
Tasca IA
Context que rep
Model recomanat (TBD)
Suggeriment de tancament
Tots els emails + notes humanes del deal
Claude (millor comprensió)
Redacció email de seguiment
Historial conversa + etapa actual
Claude / Mistral
Resum executiu d'un deal
Tot el fil complet del deal
Mistral (ràpid i econòmic)
Anàlisi per què un lead no avança
Notes + emails + dies en etapa
Claude (raonament)
Classificació ràpida de leads
Dades del municipi + emails rebuts
LLaMA (barat i ràpid)
El model s'escull en el moment d'execució. Un sol API key d'OpenRouter accedeix a tots els models. Es paga únicament el que s'usa, sense compromisos de subscripció.
8. Roadmap de Desenvolupament — 6 Setmanes
Metodologia: Gatear → Caminar → Correr. Cada fase lliura valor funcional immediat.
Fase
Durada
Lliurables
Resultat
FASE 1
Gatear
Setmanes 1-2
CRUD Municipis, Contactes i Deals. Pipeline visual Kanban. Autenticació JWT. Base de dades PostgreSQL.
CRM funcional bàsic. Pots registrar leads i moure'ls pel pipeline.
FASE 2
Caminar
Setmanes 3-4
Integració IMAP/SMTP CDmon. Vinculació email ↔ Deal. Mòdul Pagaments. Notes Humanes per Deal. Alertes renovació.
CRM complet per a ús diari. Gestió comercial i financera centralitzada.
FASE 3
Correr
Setmanes 5-6
Campanyes email híbrides. Estadístiques d'obertura. Agent IA via OpenRouter. Dashboard KPIs en temps real. Mòdul Tasques Dev.
CRM del 1%. Automatització intel·ligent amb control humà total.
9. Seguretat i Infraestructura
Capa
Implementació
Autenticació
JWT amb refresh tokens. Sessions de 24h. Logout forçat.
Transport
HTTPS forçat via Nginx. Certificat SSL Let's Encrypt automàtic.
Dades
100% al VPS propi. Compliment GDPR natiu. Cap dada a servidors tercers.
Backup
pg_dump diari automatitzat. Còpia a CDmon cada 24h.
Accés
Un sol usuari administrador en fase inicial. Arquitectura multi-rol preparada.
Correu
Credencials IMAP/SMTP encriptades en variables d'entorn (.env). Mai al codi.
10. Resum Executiu
Paràmetre
Valor
Model
B2G SaaS — Venda de llicències a Diputacions i Ajuntaments
Frontend
Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui
Backend
FastAPI (Python)
Base de dades
PostgreSQL + PostGIS (VPS propi)
Correu
IMAP/SMTP CDmon — integrat natiu, sense intermediaris
IA
OpenRouter — model flexible per tasca (TBD en execució)
Pagaments
Transferència bancària manual + gestió d'estats al CRM
Email màrqueting
Campanya híbrida (automàtica + intervenció humana)
Notes comercials
Text lliure per deal — context complet per a l'agent IA
Infraestructura
VPS propi + Docker Compose + Nginx
Cost llicències externes
0€
Temps de desenvolupament
6 setmanes (3 fases)
VEREDICTE FINAL: Aquest CRM no és una eina genèrica adaptada. És una plataforma construïda des de zero per al cas d'ús exacte de PXX: vendre sobirania digital als que encara no la tenen. La mateixa filosofia que veneu als ajuntaments, aplicada a la vostra pròpia infraestructura comercial.