# Changelog

Dates dels desplegaments i iteracions recents en el projecte **CRM PXX**.

## [2.1.0] - Desplegament de Mission Control (Fase 3/4)
### Afegits
- **AgentKimiK2 Unificat**: S'ha desglossat el classificador anterior a `services/agent_kimi_k2.py` amb mètodes d'anàlisi de silencis/bloquejos (`_call_llm` integrat) validables mitjançant pytest.
- **Sistema ARIA (A11y)**: Afegeix lectura adaptada de pantalles als xats usant la marca de navegació global `role="region"` i interjeccions amb `aria-live="polite"` durant el _polling_ del KimiChat.
- **MissionControl App UI** (`/municipis/mission-control`): Creat el modelatge 3 columnes Desktop -> 1 columna Mobile responsive, lliure de tiriants. Totes les interfícies s'adaptaran segons referències globals als mides dispositiu (Tailwind v3+).
- **Infinite Scrolling de Seguretat**: Paginat dinàmic de dades `ActivitatTimeline`. Creat control d'evasió d'apertura doble (mitjançant `loadingRef`).
- **Respostes Interactives AI**: Identificació Inline al xat pre-carregada (`"Redactar Email" -> DraftAutomàtic` / `ProgramarTrucada`).

### Corregit
- Multiplicador infinit de consultes (Rendiment) durant el muntatge incial al component de _timeline_.
- Reanomenat d'antics paquets `AIChatPanel` a l'arquitectura global actual de `KimiChat`.

## [2.0.0] - Migració a la Nova Base de Dades & Arquitectura V2 (Easypanel)
### Afegits
- Neteja de _endpoints_ v1 duplicats a FastAPI i establiment de la sintaxi V2 via taules `municipis_lifecycle` i `activitats_municipi`.
- Consolidació de la base de dates PXX al directori root local i scripts de bolcat integrats (`fresh_start_municipis.py`).
- Interfície global de Kanban implementant Drag 'n Drop estable post-migratori.
- Modals de Creació i Modificació basats en formularis ràpids via Next.js amb el framework Shadcn UI i `react-hook-form`.

### Eliminat
- Base de dades antiga de Supabase, movent tot al PostgreSQL pur autogestionat sota Easypanel amb Alembic (Pydantic models).

---
