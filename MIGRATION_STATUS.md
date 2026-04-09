# ESTAT DE LA MIGRACIÓ DE DADES (V1 → V2)

Aquest document detalla l'estat de transició entre el model legacy (V1) i la nova arquitectura unificada (V2).

## 🚀 Fase 1: Fonaments (COMPLETADA)
- [x] Disseny de `models_v2.py`.
- [x] Migracions d'Alembic inicials.
- [x] Script de migració `migrate_v1_to_v2.py` executat amb èxit.
- [x] Sistema de Prompts centralitzat (Fase 1.3).

## ✅ Fase 1.4: Deprecar Models V1 (COMPLETADA)
- [x] Fase 2.1: Arquitectura d'Agent Unificat amb Skills (COMPLETADA)
- [x] Fase 2.2: Sistema de Memòria Jeràrquica CRM - Sessió, Municipi, Global (COMPLETADA)
- [x] Marcat de `models.py` com a DEPRECATED.
- [x] Implementació de logging de detecció de queries V1 (middleware).
- [x] Auditoria d'endpoints legacy i migració d'endpoints crítics (Municipis Detail, Contactes List).

### Endpoints que encara usen V1
| Endpoint | Model Afectat | Grau d'Urgència |
| :--- | :--- | :--- |
| `/api/municipis` | `models.Municipi` | CRÍTIC |
| `/api/contactes` | `models.Contacte` | CRÍTIC |
| `/api/emails` | `models.Email` | CRÍTIC |
| `/api/deals` | `models.Deal` | ALTA |
| `/api/tasques` | `models.Tasca` | MITJANA |
| `/api/pagaments` | `models.Pagament` | BAIXA |

## 📅 Pla de Migració d'Endpoints

### Setmana 1: Endpoints de Consulta (Lectura)
1. Migrar `GET /api/municipis` a `models_v2.MunicipiLifecycle`.
2. Migrar `GET /api/contactes` a `models_v2.ContacteV2`.
3. Validar que el frontend (Next.js) llegeix correctament els nous UUIDs.

### Setmana 2: Endpoints d'Escriptura
1. Migrar `POST /api/municipis`.
2. Migrar `POST /api/contactes`.
3. Implementar logic de sincronització bidireccional si fos necessari (opcional).

### Deadline d'Eliminació (Fase C)
* **Eliminació de `models.py`**: Prevista per al 01/05/2026.
* **Eliminació de taules V1 a la DB**: Prevista per al 15/05/2026.

---
*Darrera actualització: 09/04/2026*
