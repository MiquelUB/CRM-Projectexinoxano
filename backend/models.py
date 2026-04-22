
import uuid
import enum
from sqlalchemy import Column, String, Boolean, Integer, Text, Numeric, Date, ForeignKey, DateTime, Enum, Float, ARRAY, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from database import Base

# --- Enums ---

class TipusActivitat(str, enum.Enum):
    nota_manual = "nota_manual"
    email_enviat = "email_enviat"
    email_rebut = "email_rebut"
    trucada = "trucada"
    reunio = "reunio"
    demo = "demo"
    pagament = "pagament"
    canvi_etapa = "canvi_etapa"
    sistema = "sistema"

class GeografiaEnum(str, enum.Enum):
    muntanya = "muntanya"
    mar = "mar"
    interior = "interior"
    city = "city"

class EtapaFunnelEnum(str, enum.Enum):
    lead = "lead"
    research = "research"
    contacte = "contacte"
    demo_pendent = "demo_pendent"
    demo_ok = "demo_ok"
    oferta = "oferta"
    documentacio = "documentacio"
    aprovacio = "aprovacio"
    contracte = "contracte"
    client = "client"
    pausa = "pausa"
    perdut = "perdut"

class BlockerEnum(str, enum.Enum):
    alcalde = "alcalde"
    tecnic = "tecnic"
    cfo = "cfo"
    temporitzacio = "temporitzacio"
    cap = "cap"

class TemperaturaEnum(str, enum.Enum):
    fred = "fred"
    templat = "templat"
    calent = "calent"
    bullent = "bullent"

class PlaEnum(str, enum.Enum):
    Roure = "Roure"
    Mirador = "Mirador"
    Territori = "Territori"

class TipusSequenciaEnum(str, enum.Enum):
    prospeccio = "prospeccio"
    seguiment = "seguiment"
    reactivacio = "reactivacio"

class EstatSequenciaEnum(str, enum.Enum):
    pendent = "pendent"
    preparat = "preparat"
    enviat = "enviat"
    cancelat = "cancelat"
    error = "error"

class EstatFinalEnum(str, enum.Enum):
    client = "client"
    perdut = "perdut"
    pausa = "pausa"

class CarrecEnum(str, enum.Enum):
    alcalde = "alcalde"
    regidor_turisme = "regidor_turisme"
    tecnic = "tecnic"
    cfo = "cfo"
    regidor_cultura = "regidor_cultura"
    altre = "altre"

class ToComunicacioEnum(str, enum.Enum):
    formal = "formal"
    proxim = "proxim"
    tecnic = "tecnic"

class SentimentEnum(str, enum.Enum):
    positiu = "positiu"
    neutre = "neutre"
    negatiu = "negatiu"
    confus = "confus"

class ActorEnum(str, enum.Enum):
    alcalde = "alcalde"
    tecnic = "tecnic"
    cfo = "cfo"

# --- Common Models ---

class Usuari(Base):
    __tablename__ = "usuaris"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nom = Column(String(100), nullable=False)
    rol = Column(String(50), default="admin")
    actiu = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# --- Unified Domain Models ---

class Municipi(Base):
    __tablename__ = "municipis"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String(100), nullable=False, index=True)
    comarca = Column(String(50))
    poblacio = Column(String(100))
    geografia = Column(Enum(GeografiaEnum, name="geografia", native_enum=True), nullable=True)
    
    tipus = Column(String(50), default='ajuntament')
    provincia = Column(String(50), default='Barcelona')
    codi_postal = Column(String(20))
    web = Column(String(255))
    telefon = Column(String(50))
    adreca = Column(Text)
    
    diagnostic_digital = Column(JSONB, default={})
    angle_personalitzacio = Column(Text)
    
    etapa_actual = Column(Enum(EtapaFunnelEnum, name="etapa_funnel", native_enum=True), default=EtapaFunnelEnum.research, index=True)
    historial_etapes = Column(JSONB, default=[])
    
    blocker_actual = Column(Enum(BlockerEnum, name="blocker", native_enum=True), default=BlockerEnum.cap)
    temperatura = Column(Enum(TemperaturaEnum, name="temperatura", native_enum=True), default=TemperaturaEnum.fred)
    dies_etapa_actual = Column(Integer, default=0)
    
    data_conversio = Column(DateTime, nullable=True)
    pla_contractat = Column(Enum(PlaEnum, name="pla", native_enum=True), nullable=True)
    estat_final = Column(Enum(EstatFinalEnum, name="estat_final", native_enum=True), nullable=True)
    
    valor_setup = Column(Numeric(10, 2), default=0)
    valor_llicencia = Column(Numeric(10, 2), default=0)
    proper_pas = Column(Text)
    prioritat = Column(String(20), default="mitjana")
    data_seguiment = Column(DateTime, nullable=True)
    notes_humanes = Column(Text, nullable=True)
    
    actor_principal_id = Column(UUID(as_uuid=True), ForeignKey("contactes.id"), nullable=True)
    municipi_v1_id = Column(UUID(as_uuid=True), nullable=True) # Per referència històrica
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    data_ultima_accio = Column(DateTime(timezone=True), server_default=func.now())
    usuari_asignat = Column(String(50), default='fundador')
    
    # Relacions
    actor_principal = relationship("Contacte", foreign_keys=[actor_principal_id], lazy="joined")
    contactes = relationship("Contacte", back_populates="municipi", lazy="joined", cascade="all, delete-orphan", foreign_keys="[Contacte.municipi_id]")
    emails = relationship("Email", back_populates="municipi", cascade="all, delete-orphan")
    trucades = relationship("Trucada", back_populates="municipi", cascade="all, delete-orphan")
    reunions = relationship("Reunio", back_populates="municipi", cascade="all, delete-orphan")
    activitats = relationship("Activitat", back_populates="municipi", cascade="all, delete-orphan")
    tasques = relationship("Tasca", back_populates="municipi", cascade="all, delete-orphan")

class Contacte(Base):
    __tablename__ = "contactes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis.id"), nullable=False)
    
    nom = Column(String(100), nullable=False)
    carrec = Column(String(100), default="altre")
    email = Column(String(100))
    telefon = Column(String(20))
    
    actiu = Column(Boolean, default=True)
    principal = Column(Boolean, default=False)
    
    angles_exitosos = Column(JSONB, default=[])
    angles_fallits = Column(JSONB, default=[])
    moment_optimal = Column(String(10))
    to_preferit = Column(String(50), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    municipi = relationship("Municipi", back_populates="contactes", foreign_keys="[Contacte.municipi_id]")

class Email(Base):
    __tablename__ = "emails"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis.id"), nullable=True)
    contacte_id = Column(UUID(as_uuid=True), ForeignKey("contactes.id"), nullable=True)
    
    from_address = Column(String(255))
    to_address = Column(String(255))
    assumpte = Column(String(200))
    cos = Column(Text)
    direccio = Column(String(10)) # 'OUT' or 'IN'
    llegit = Column(Boolean, default=False)
    message_id_extern = Column(String(500), unique=True, nullable=True)
    tracking_token = Column(String(100), unique=True, nullable=True)
    
    data_enviament = Column(DateTime(timezone=True), server_default=func.now())
    
    obert = Column(Boolean, default=False)
    data_obertura = Column(DateTime(timezone=True))
    cops_obert = Column(Integer, default=0)
    respost = Column(Boolean, default=False)
    data_resposta = Column(DateTime(timezone=True))
    
    sentiment_resposta = Column(String(20), nullable=True)
    intents_detectats = Column(JSONB, default=[])
    actor_probable = Column(String(20), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    municipi = relationship("Municipi", back_populates="emails")

class Trucada(Base):
    __tablename__ = "trucades"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis.id"), nullable=False)
    contacte_id = Column(UUID(as_uuid=True), ForeignKey("contactes.id"), nullable=True)
    
    data = Column(DateTime(timezone=True), server_default=func.now())
    durada_minuts = Column(Integer, default=0)
    qui_va_contestar = Column(Enum(ActorEnum, name="actor_respuesta", native_enum=True), nullable=True)
    
    notes_breus = Column(Text)
    seguent_accio_sugerida = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    municipi = relationship("Municipi", back_populates="trucades")

class Reunio(Base):
    __tablename__ = "reunions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis.id"), nullable=False)
    contacte_id = Column(UUID(as_uuid=True), ForeignKey("contactes.id"), nullable=True)
    
    data = Column(DateTime(timezone=True))
    tipus = Column(String(20))
    assistents = Column(JSONB, default=[])
    
    aar_completat = Column(Boolean, default=False)
    notes_aar = Column(Text)
    poi_mes_reaccio = Column(String(100))
    objeccio_principal = Column(String(100))
    cta_final = Column(String(200))
    temperatura_post = Column(Enum(TemperaturaEnum, name="temperatura_post", native_enum=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    municipi = relationship("Municipi", back_populates="reunions")



class Activitat(Base):
    __tablename__ = "activitats"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis.id"), nullable=False, index=True)
    contacte_id = Column(UUID(as_uuid=True), ForeignKey("contactes.id"), nullable=True)
    
    tipus_activitat = Column(Enum(TipusActivitat, name="tipus_activitat", native_enum=True), nullable=False, index=True)
    data_activitat = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    contingut = Column(JSONB, default={})
    notes_comercial = Column(Text)
    etiquetes = Column(ARRAY(String), default=[])
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    municipi = relationship("Municipi", back_populates="activitats")



class Tasca(Base):
    __tablename__ = "tasques"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis.id"), nullable=False)
    
    titol = Column(String(200), nullable=False)
    descripcio = Column(Text)
    data_venciment = Column(DateTime)
    prioritat = Column(Integer, default=2) # 1: baixa, 2: mitjana, 3: alta
    estat = Column(String(20), default="pendent")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    municipi = relationship("Municipi", back_populates="tasques")

# --- Llicències i Pagaments (Heretats de V1 però apuntant a Municipis) ---

class Llicencia(Base):
    __tablename__ = "llicencies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("municipis.id"), nullable=False, unique=True)
    data_inici = Column(Date, nullable=False)
    data_renovacio = Column(Date, nullable=True)
    estat = Column(String(50), default="activa")
    import_ = Column("import", Numeric(10, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    municipi = relationship("Municipi", foreign_keys=[deal_id], backref="llicencia_rel", uselist=False)

class Pagament(Base):
    __tablename__ = "pagaments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    llicencia_id = Column(UUID(as_uuid=True), ForeignKey("llicencies.id"), nullable=False)
    import_ = Column("import", Numeric(10, 2), nullable=False)
    tipus = Column(String(50), default="llicencia_anual")
    estat = Column(String(50), default="emes")
    data_emisio = Column(Date, nullable=False)
    data_limit = Column(Date, nullable=True)
    data_confirmacio = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    llicencia = relationship("Llicencia", backref="pagaments")
