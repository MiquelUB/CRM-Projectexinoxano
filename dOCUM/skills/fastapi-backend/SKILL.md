---
name: fastapi-backend
description: Guides creation of FastAPI endpoints, SQLAlchemy models, and Pydantic schemas for the CRM PXX backend. Use when creating or editing any backend Python file including models, routers, schemas, or database logic.
---

# FastAPI Backend — Convencions CRM PXX

Aplica aquest skill sempre que treballis en qualsevol fitxer Python del backend.

## Estructura d'un Router (patró estàndard)

Cada mòdul a `routers/` segueix sempre aquest patró:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database import get_db
from auth import get_current_user
import models, schemas

router = APIRouter(prefix="/nom-modul", tags=["Nom Mòdul"])

@router.get("/", response_model=schemas.PaginatedResponse)
def llistar(
    page: int = 1,
    limit: int = 20,
    cerca: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Lògica aquí
    pass
```

## Models SQLAlchemy (patró obligatori)

```python
import uuid
from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class NomModel(Base):
    __tablename__ = "nom_taula"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # ... camps específics ...
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
```

**Regla:** Tots els models hereten de Base i tenen id (UUID), created_at i updated_at. Sempre.

## Schemas Pydantic (tres schemas per entitat)

```python
from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

# 1. Base — camps comuns
class NomBase(BaseModel):
    camp_obligatori: str
    camp_opcional: Optional[str] = None

# 2. Create — per a POST (sense id ni timestamps)
class NomCreate(NomBase):
    pass

# 3. Response — per a GET (inclou id i timestamps)
class NomResponse(NomBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

## Gestió d'Errors

Sempre en català. Codis HTTP estàndard:

```python
# 404
raise HTTPException(status_code=404, detail="Municipi no trobat")

# 400
raise HTTPException(status_code=400, detail="L'email ja existeix al sistema")

# 403
raise HTTPException(status_code=403, detail="No tens permisos per fer aquesta acció")

# 409
raise HTTPException(status_code=409, detail="Ja existeix un deal actiu per aquest municipi")
```

## Paginació Estàndard

Totes les llistes retornen aquest format:

```python
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    limit: int
    total_pages: int
```

## Variables d'Entorn (.env)

```
DATABASE_URL=postgresql://pxx_admin:pxx_secret_local@localhost:5432/crm_pxx
SECRET_KEY=string_aleatori_molt_llarg
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
OPENROUTER_API_KEY=sk-or-...
IMAP_HOST=mail.cdmon.com
IMAP_USER=crm@projectexinoxano.cat
IMAP_PASSWORD=contrasenya_segura
SMTP_HOST=mail.cdmon.com
SMTP_PORT=587
```

## Checklist abans de fer commit

- [ ] Cap secret al codi (tot a .env)
- [ ] Missatges d'error en català
- [ ] Tots els endpoints protegits amb Depends(get_current_user)
- [ ] Response models declarats a tots els endpoints
- [ ] IDs UUID en tots els models nous
