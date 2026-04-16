from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any, Dict
from uuid import UUID
from datetime import datetime
from models import EtapaFunnelEnum, TemperaturaEnum, CarrecEnum, ToComunicacioEnum, TipusActivitat

class Token(BaseModel):
    access_token: str
    token_type: str

class UsuariBase(BaseModel):
    email: EmailStr
    nom: str
    rol: str = "comercial"
    actiu: bool = True

class UsuariCreate(UsuariBase):
    password: str

class UsuariOut(UsuariBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class ContacteCreate(BaseModel):
    nom: str
    carrec: Optional[str] = "altre"
    email: Optional[EmailStr] = None
    telefon: Optional[str] = None
    principal: bool = False

class ContacteOut(BaseModel):
    id: UUID
    municipi_id: UUID
    nom: str
    carrec: Optional[str] = "altre"
    email: Optional[Optional[str]] = None
    telefon: Optional[str] = None
    principal: bool
    actiu: bool

    class Config:
        from_attributes = True

class ContactePaginationOut(BaseModel):
    items: List[ContacteOut]
    total: int
    page: int

class ContacteUpdate(BaseModel):
    nom: Optional[str] = None
    carrec: Optional[str] = None
    email: Optional[EmailStr] = None
    telefon: Optional[str] = None
    principal: Optional[bool] = None
    actiu: Optional[bool] = None

class MunicipiCreate(BaseModel):
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

class MunicipiOut(BaseModel):
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
    valor_setup: float = 0
    valor_llicencia: float = 0
    prioritat: str = "mitjana"
    actor_principal: Optional[ContacteOut] = None
    proper_pas: Optional[str] = None
    data_seguiment: Optional[datetime] = None
    notes_humanes: Optional[str] = None
    created_at: datetime
    data_ultima_accio: Optional[datetime] = None

    class Config:
        from_attributes = True

class MunicipiPaginationOut(BaseModel):
    items: List[MunicipiOut]
    total: int

class MunicipiDetailOut(MunicipiOut):
    contactes: List[ContacteOut] = []

class ActivitatCreate(BaseModel):
    municipi_id: UUID
    contacte_id: Optional[UUID] = None
    tipus_activitat: TipusActivitat
    data_activitat: Optional[datetime] = None
    contingut: Optional[dict] = {}
    notes_comercial: Optional[str] = None
    generat_per_ia: bool = False
    etiquetes: List[str] = []

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

class EmailOut(BaseModel):
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

class TascaCreate(BaseModel):
    municipi_id: UUID
    titol: str
    descripcio: Optional[str] = None
    data_venciment: datetime
    prioritat: Optional[int] = 2

class TascaOut(BaseModel):
    id: UUID
    municipi_id: UUID
    titol: str
    descripcio: Optional[str] = None
    data_venciment: datetime
    prioritat: int
    estat: str
    created_at: datetime

    class Config:
        from_attributes = True

class EmailDraftCreateRequest(BaseModel):
    tipus: str
    contacte_id: Optional[UUID] = None

class EmailDraftEditRequest(BaseModel):
    subject: str
    cos: str
    canvis: Optional[dict] = {}

class EmailDraftSelectVariantRequest(BaseModel):
    variant_id: int

class EmailDraftSendRequest(BaseModel):
    mode: str
    data_programada: Optional[datetime] = None

class EmailSequenciaGenerateRequest(BaseModel):
    contacte_id: Optional[UUID] = None

class AgentRedactarEmailRequest(BaseModel):
    municipi_id: Optional[UUID] = None
    deal_id: Optional[UUID] = None
    contacte_id: Optional[UUID] = None
    instruccions: str
