from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date
from decimal import Decimal

# --- Usuari ---
class UsuariBase(BaseModel):
    email: EmailStr
    nom: str
    rol: str = "admin"
    actiu: bool = True

class UsuariCreate(UsuariBase):
    password: str

class UsuariOut(UsuariBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# --- Municipi ---
class MunicipiBase(BaseModel):
    nom: str
    tipus: str
    provincia: Optional[str] = None
    poblacio: Optional[str] = None
    codi_postal: Optional[str] = None
    web: Optional[str] = None
    telefon: Optional[str] = None
    adreca: Optional[str] = None
    notes: Optional[str] = None

class MunicipiCreate(MunicipiBase):
    pass

class MunicipiUpdate(BaseModel):
    nom: Optional[str] = None
    tipus: Optional[str] = None
    provincia: Optional[str] = None
    poblacio: Optional[str] = None
    codi_postal: Optional[str] = None
    web: Optional[str] = None
    telefon: Optional[str] = None
    adreca: Optional[str] = None
    notes: Optional[str] = None

class MunicipiOut(MunicipiBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MunicipiListResponse(BaseModel):
    items: List[MunicipiOut]
    total: int
    page: int

# --- Contacte ---
class ContacteBase(BaseModel):
    municipi_id: UUID
    nom: str
    carrec: Optional[str] = None
    email: Optional[EmailStr] = None
    telefon: Optional[str] = None
    linkedin: Optional[str] = None
    notes_humanes: Optional[str] = None
    actiu: bool = True

class ContacteCreate(ContacteBase):
    pass

class ContacteUpdate(BaseModel):
    municipi_id: Optional[UUID] = None
    nom: Optional[str] = None
    carrec: Optional[str] = None
    email: Optional[EmailStr] = None
    telefon: Optional[str] = None
    linkedin: Optional[str] = None
    notes_humanes: Optional[str] = None
    actiu: Optional[bool] = None

class ContacteOut(ContacteBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    municipi: Optional[MunicipiOut] = None
    
    class Config:
        from_attributes = True

class ContacteShortOut(ContacteBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ContacteListResponse(BaseModel):
    items: List[ContacteOut]
    total: int
    page: int

# --- Deal ---
class DealBase(BaseModel):
    municipi_id: UUID
    contacte_id: Optional[UUID] = None
    titol: str
    etapa: str = "prospecte"
    valor_setup: Decimal = Field(default=0, decimal_places=2)
    valor_llicencia: Decimal = Field(default=0, decimal_places=2)
    prioritat: str = "mitjana"
    proper_pas: Optional[str] = None
    data_seguiment: Optional[date] = None
    data_tancament_prev: Optional[date] = None
    data_tancament_real: Optional[date] = None
    motiu_perdua: Optional[str] = None
    notes_humanes: Optional[str] = None

class DealCreate(DealBase):
    pass

class DealUpdate(BaseModel):
    municipi_id: Optional[UUID] = None
    contacte_id: Optional[UUID] = None
    titol: Optional[str] = None
    etapa: Optional[str] = None
    valor_setup: Optional[Decimal] = None
    valor_llicencia: Optional[Decimal] = None
    prioritat: Optional[str] = None
    proper_pas: Optional[str] = None
    data_seguiment: Optional[date] = None
    data_tancament_prev: Optional[date] = None
    data_tancament_real: Optional[date] = None
    motiu_perdua: Optional[str] = None
    notes_humanes: Optional[str] = None

class DealOut(DealBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    municipi: Optional[MunicipiOut] = None
    contacte: Optional[ContacteOut] = None
    
    class Config:
        from_attributes = True

class DealShortOut(DealBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# --- Detail Schemas to avoid Circularity ---

class MunicipiDetailOut(MunicipiOut):
    contactes: List[ContacteShortOut] = []
    deals: List[DealShortOut] = []
    
    class Config:
        from_attributes = True

class DealActivitatOut(BaseModel):
    id: UUID
    deal_id: UUID
    tipus: str
    descripcio: str
    valor_anterior: Optional[str] = None
    valor_nou: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class DealDetailOut(DealOut):
    activitats: List[DealActivitatOut] = []
    
    class Config:
        from_attributes = True

class DealKpis(BaseModel):
    total_deals: int
    valor_total_pipeline: float
    deals_per_tancar_aquest_mes: int
    deals_sense_activitat_14_dies: int

class DealListResponse(BaseModel):
    items: List[DealDetailOut]
    total: int
    kpis: Optional[DealKpis] = None

# --- Auth ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    
class LoginSchema(BaseModel):
    email: str
    password: str

# --- Email ---
class EmailBase(BaseModel):
    deal_id: Optional[UUID] = None
    contacte_id: Optional[UUID] = None
    campanya_id: Optional[UUID] = None
    from_address: str
    to_address: str
    assumpte: str
    cos: Optional[str] = None
    direccio: str
    llegit: bool = False
    sincronitzat: bool = False
    message_id_extern: Optional[str] = None
    data_email: datetime
    tracking_token: Optional[str] = None
    obert: bool = False
    data_obertura: Optional[datetime] = None
    nombre_obertures: int = 0
    ip_obertura: Optional[str] = None

class EmailCreate(BaseModel):
    pass

class EmailUpdate(BaseModel):
    deal_id: Optional[UUID] = None
    llegit: Optional[bool] = None

class EmailOut(EmailBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class EmailResponse(BaseModel):
    items: List[EmailOut]
    total: int
    page: int
    total_pages: int

class EmailPendentsResponse(BaseModel):
    items: List[EmailOut]
    total: int

# --- Agent IA ---
class AgentRedactarEmailRequest(BaseModel):
    deal_id: Optional[UUID] = None
    instruccions: Optional[str] = None
    model: str = "anthropic/claude-3.5-sonnet"
    to_address: Optional[str] = None
    contacte_id: Optional[UUID] = None

class AgentRedactarEmailResponse(BaseModel):
    assumpte: str
    cos_text: str
    model_usat: str
    tokens_usats: int

class AgentAnalitzarDealRequest(BaseModel):
    deal_id: UUID
    model: str = "anthropic/claude-3.5-sonnet"

class AgentAnalitzarDealResponse(BaseModel):
    obstacle_principal: str
    proper_pas_recomanat: str
    missatge_clau: str
    urgencia: str
    model_usat: str

class AgentResumDealRequest(BaseModel):
    deal_id: UUID
    model: str = "mistralai/mistral-small-3.1-24b-instruct"

class AgentResumDealResponse(BaseModel):
    resum: str
    model_usat: str

# --- Pagament ---
class PagamentBase(BaseModel):
    llicencia_id: UUID
    import_: Decimal = Field(alias="import")
    tipus: str
    estat: str = "emes"
    data_emisio: date
    data_limit: Optional[date] = None
    data_confirmacio: Optional[date] = None
    notes: Optional[str] = None

class PagamentCreate(BaseModel):
    llicencia_id: UUID
    import_: Decimal = Field(alias="import")
    tipus: str
    data_emisio: date
    data_limit: Optional[date] = None

class PagamentUpdate(BaseModel):
    estat: Optional[str] = None
    data_confirmacio: Optional[date] = None
    notes: Optional[str] = None

class PagamentOut(PagamentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True

# --- Llicencia ---
class LlicenciaBase(BaseModel):
    deal_id: UUID
    data_inici: date
    data_renovacio: date
    estat: str = "activa"
    notes: Optional[str] = None

class LlicenciaCreate(LlicenciaBase):
    pass

class LlicenciaUpdate(BaseModel):
    estat: Optional[str] = None
    data_renovacio: Optional[date] = None
    notes: Optional[str] = None

class LlicenciaOut(LlicenciaBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    pagaments: List[PagamentOut] = []
    
    class Config:
        from_attributes = True

class LlicenciaListResponse(BaseModel):
    items: List[LlicenciaOut]
    total: int

class PagamentKpis(BaseModel):
    arr_total: float
    pendent: float
    vencut: float
    proper_30: int

class PagamentListResponse(BaseModel):
    items: List[PagamentOut]
    total: int
    resum: Optional[PagamentKpis] = None

class TascaBase(BaseModel):
    titol: str
    descripcio: Optional[str] = None
    data_venciment: date
    tipus: str = "altre"
    prioritat: str = "mitjana"
    deal_id: Optional[UUID] = None
    contacte_id: Optional[UUID] = None
    municipi_id: Optional[UUID] = None
    usuari_id: Optional[UUID] = None

class TascaCreate(TascaBase):
    pass

class TascaUpdate(BaseModel):
    titol: Optional[str] = None
    descripcio: Optional[str] = None
    data_venciment: Optional[date] = None
    tipus: Optional[str] = None
    prioritat: Optional[str] = None
    estat: Optional[str] = None

class TascaOut(TascaBase):
    id: UUID
    estat: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TascaListResponse(BaseModel):
    items: List[TascaOut]
    total: int
