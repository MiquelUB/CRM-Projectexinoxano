from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime
from models_v2 import EtapaFunnelEnum, TemperaturaEnum, CarrecEnum, ToComunicacioEnum

class ContacteCreate(BaseModel):
    nom: str
    carrec: CarrecEnum
    email: Optional[EmailStr] = None
    telefon: Optional[str] = None
    principal: bool = False

class ContacteOut(BaseModel):
    id: UUID
    municipi_id: UUID
    nom: str
    carrec: CarrecEnum
    email: Optional[str] = None
    telefon: Optional[str] = None
    principal: bool
    actiu: bool

    class Config:
        from_attributes = True

class MunicipiLifecycleCreate(BaseModel):
    nom: str
    comarca: Optional[str] = None
    poblacio: Optional[str] = None
    tipus: Optional[str] = "ajuntament"
    provincia: Optional[str] = "Barcelona"
    codi_postal: Optional[str] = None
    web: Optional[str] = None
    telefon: Optional[str] = None
    adreca: Optional[str] = None
    geografia: Optional[str] = None
    notes_humanes: Optional[str] = None

class MunicipiLifecycleOut(BaseModel):
    id: UUID
    nom: str
    comarca: Optional[str] = None
    poblacio: Optional[str] = None
    tipus: Optional[str] = "ajuntament"
    provincia: Optional[str] = "Barcelona"
    codi_postal: Optional[str] = None
    web: Optional[str] = None
    telefon: Optional[str] = None
    adreca: Optional[str] = None
    geografia: Optional[str] = None
    diagnostic_digital: Optional[dict] = None
    angle_personalitzacio: Optional[str] = None
    etapa_actual: EtapaFunnelEnum
    temperatura: TemperaturaEnum
    dies_etapa_actual: int
    actor_principal_id: Optional[UUID] = None
    # Nous camps per al pipeline
    valor_setup: float = 0
    valor_llicencia: float = 0
    prioritat: str = "mitjana"
    proper_pas: Optional[str] = None
    data_seguiment: Optional[datetime] = None
    notes_humanes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @property
    def updated_at_fallback(self):
        return self.updated_at or self.created_at

class MunicipiPaginationOut(BaseModel):
    items: List[MunicipiLifecycleOut]
    total: int

class MunicipiLifecycleDetailOut(MunicipiLifecycleOut):
    contactes: List[ContacteOut] = []
    # communication counts optional
    # emails: List[Any] = []

class AccioCreate(BaseModel):
    accio: str # e.g., 'trucar', 'enviar_email'
    notes: Optional[str] = None
    detall: Optional[dict] = None # holds parsed details

class EmailDraftCreateRequest(BaseModel):
    tipus: str # email_1_prospeccio, email_2_dolor, etc.
    contacte_id: Optional[UUID] = None

class EmailDraftEditRequest(BaseModel):
    subject: str
    cos: str
    canvis: Optional[dict] = {}

class EmailDraftSelectVariantRequest(BaseModel):
    variant_id: int

class EmailDraftSendRequest(BaseModel):
    mode: str # 'immediat', 'programat'
    data_programada: Optional[datetime] = None

class EmailSequenciaGenerateRequest(BaseModel):
    contacte_id: Optional[UUID] = None

# --- Activitats V2 ---

from models_v2 import TipusActivitat

class ActivitatCreate(BaseModel):
    municipi_id: UUID
    contacte_id: Optional[UUID] = None
    deal_id: Optional[UUID] = None
    tipus_activitat: TipusActivitat
    data_activitat: Optional[datetime] = None
    contingut: Optional[dict] = {}
    notes_comercial: Optional[str] = None
    generat_per_ia: bool = False
    etiquetes: List[str] = []

class ActivitatUpdate(BaseModel):
    notes_comercial: Optional[str] = None
    etiquetes: Optional[List[str]] = None

class ActivitatOut(BaseModel):
    id: UUID
    municipi_id: UUID
    contacte_id: Optional[UUID] = None
    tipus_activitat: TipusActivitat
    data_activitat: datetime
    contingut: dict
    notes_comercial: Optional[str] = None
    generat_per_ia: bool
    etiquetes: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ActivitatPaginationOut(BaseModel):
    items: List[ActivitatOut]
    total: int
    page: int
    pages: int

class ContactePaginationOut(BaseModel):
    items: List[ContacteOut]
    total: int
    page: int

class EmailV2Out(BaseModel):
    id: UUID
    municipi_id: Optional[UUID] = None
    contacte_id: Optional[UUID] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    assumpte: Optional[str] = None
    cos: Optional[str] = None
    direccio: Optional[str] = None
    data_enviament: datetime
    obert: bool = False
    respost: bool = False
    
    class Config:
        from_attributes = True
