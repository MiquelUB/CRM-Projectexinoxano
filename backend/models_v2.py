import uuid
from sqlalchemy import Column, String, Boolean, Integer, Text, Numeric, Date, ForeignKey, DateTime, Enum, Float, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from database import Base
import enum

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

# --- Models ---

class MunicipiLifecycle(Base):
    __tablename__ = "municipis_lifecycle"
    
    # IDENTITAT
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String(100), nullable=False, index=True)
    comarca = Column(String(50))
    poblacio = Column(Integer)
    geografia = Column(Enum(GeografiaEnum, name="geografia", native_enum=False), nullable=True)
    
    # DIAGNÒSTIC
    diagnostic_digital = Column(JSONB, default={})  # app_propia, google_maps_pois, wikiloc_rutes, buit_digital, patrimoni, context_politic
    angle_personalitzacio = Column(Text)
    
    # FUNNEL
    etapa_actual = Column(Enum(EtapaFunnelEnum, name="etapa_funnel", native_enum=False), default=EtapaFunnelEnum.research, index=True)
    historial_etapes = Column(JSONB, default=[]) # e.g. [{"etapa": "research", "data_inici": "...", "data_fi": "...", "notes": "..."}]
    
    blocker_actual = Column(Enum(BlockerEnum, name="blocker", native_enum=False), default=BlockerEnum.cap)
    temperatura = Column(Enum(TemperaturaEnum, name="temperatura", native_enum=False), default=TemperaturaEnum.fred)
    dies_etapa_actual = Column(Integer, default=0)
    
    # POST-VENDA (Dades tancament)
    data_conversio = Column(DateTime, nullable=True)
    pla_contractat = Column(Enum(PlaEnum, name="pla", native_enum=False), nullable=True)
    estat_final = Column(Enum(EstatFinalEnum, name="estat_final", native_enum=False), nullable=True)
    
    # Dades econòmiques i tàctiques (migrades de Deal)
    valor_setup = Column(Numeric(10, 2), default=0)
    valor_llicencia = Column(Numeric(10, 2), default=0)
    proper_pas = Column(Text)
    prioritat = Column(String(20), default="mitjana") # 'alta' | 'mitjana' | 'baixa'
    data_seguiment = Column(DateTime, nullable=True)
    notes_humanes = Column(Text, nullable=True)
    
    actor_principal_id = Column(UUID(as_uuid=True), ForeignKey("contactes_v2.id"), nullable=True)
    
    # METADADES
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    data_ultima_accio = Column(DateTime(timezone=True), server_default=func.now())
    usuari_asignat = Column(String(50), default='fundador')
    
    # Relacions
    contactes = relationship("ContacteV2", back_populates="municipi", lazy="joined", cascade="all, delete-orphan", foreign_keys="[ContacteV2.municipi_id]")
    emails = relationship("EmailV2", back_populates="municipi", cascade="all, delete-orphan")
    trucades = relationship("TrucadaV2", back_populates="municipi", cascade="all, delete-orphan")
    reunions = relationship("ReunioV2", back_populates="municipi", cascade="all, delete-orphan")
    email_drafts = relationship("EmailDraftV2", back_populates="municipi", cascade="all, delete-orphan", foreign_keys="[EmailDraftV2.municipi_id]")
    sequencia_emails = relationship("EmailSequenciaV2", back_populates="municipi", cascade="all, delete-orphan", foreign_keys="[EmailSequenciaV2.municipi_id]")
    activitats = relationship("ActivitatsMunicipi", back_populates="municipi", cascade="all, delete-orphan")
    agent_memories = relationship("AgentMemoryV2", back_populates="municipi", cascade="all, delete-orphan")
    tasques = relationship("TascaV2", back_populates="municipi", cascade="all, delete-orphan")


class ContacteV2(Base):
    __tablename__ = "contactes_v2"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis_lifecycle.id"), nullable=False)
    
    nom = Column(String(100), nullable=False)
    carrec = Column(Enum(CarrecEnum, name="carrec", native_enum=False), nullable=False)
    email = Column(String(100))
    telefon = Column(String(20))
    
    actiu = Column(Boolean, default=True)
    principal = Column(Boolean, default=False)
    
    # Memòria específica
    angles_exitosos = Column(JSONB, default=[])
    angles_fallits = Column(JSONB, default=[])
    moment_optimal = Column(String(10))  # e.g., "10:00"
    to_preferit = Column(Enum(ToComunicacioEnum, name="to_comunicacio", native_enum=False), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacions
    municipi = relationship("MunicipiLifecycle", back_populates="contactes", foreign_keys="[ContacteV2.municipi_id]")


# --- Comunicacions ---

class EmailV2(Base):
    __tablename__ = "emails_v2"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis_lifecycle.id"), nullable=False)
    
    data_enviament = Column(DateTime(timezone=True), server_default=func.now())
    assumpte = Column(String(200))
    cos = Column(Text)
    
    # Tracking
    obert = Column(Boolean, default=False)
    data_obertura = Column(DateTime(timezone=True))
    cops_obert = Column(Integer, default=0)
    respost = Column(Boolean, default=False)
    data_resposta = Column(DateTime(timezone=True))
    
    # Anàlisi IA
    sentiment_resposta = Column(Enum(SentimentEnum, name="sentiment", native_enum=False), nullable=True)
    intents_detectats = Column(JSONB, default=[])
    actor_probable = Column(Enum(ActorEnum, name="actor", native_enum=False), nullable=True)
    
    # Relacions
    municipi = relationship("MunicipiLifecycle", back_populates="emails")


class TrucadaV2(Base):
    __tablename__ = "trucades_v2"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis_lifecycle.id"), nullable=False)
    
    data = Column(DateTime(timezone=True), server_default=func.now())
    durada_minuts = Column(Integer, default=0)
    qui_va_contestar = Column(Enum(ActorEnum, name="actor_respuesta", native_enum=False), nullable=True)  # alcalde, tecnic, cfo, etc.
    
    notes_breus = Column(Text)
    resum_ia = Column(Text)
    seguent_accio_sugerida = Column(Text)
    
    # Relacions
    municipi = relationship("MunicipiLifecycle", back_populates="trucades")


class ReunioV2(Base):
    __tablename__ = "reunions_v2"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis_lifecycle.id"), nullable=False)
    
    data = Column(DateTime(timezone=True))
    tipus = Column(String(20)) # 'demo', 'seguiment', 'negociacio'
    assistents = Column(JSONB, default=[]) # ["alcalde", "tecnic"]
    
    # Post-reunió
    aar_completat = Column(Boolean, default=False)
    notes_aar = Column(Text)
    poi_mes_reaccio = Column(String(100))
    objeccio_principal = Column(String(100))
    cta_final = Column(String(200))
    temperatura_post = Column(Enum(TemperaturaEnum, name="temperatura_post", native_enum=False), nullable=True)
    
    # Relacions
    municipi = relationship("MunicipiLifecycle", back_populates="reunions")


# --- EmailDraft & Seqüència ---

class EstatDraftEnum(str, enum.Enum):
    esborrany = "esborrany"
    revisat = "revisat"
    enviat = "enviat"
    programat = "programat"

class TipusSequenciaEnum(str, enum.Enum):
    prospeccio = "prospeccio"
    seguiment = "seguiment"
    nurture = "nurture"
    recuperacio = "recuperacio"

class EstatSequenciaEnum(str, enum.Enum):
    pendent = "pendent"
    preparant = "preparant"
    preparat = "preparat"
    programat = "programat"
    enviat = "enviat"
    obert = "obert"
    respost = "respost"
    no_obert = "no_obert"
    cancelat = "cancelat"

class EmailDraftV2(Base):
    __tablename__ = "email_drafts_v2"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis_lifecycle.id"), nullable=False)
    contacte_id = Column(UUID(as_uuid=True), ForeignKey("contactes_v2.id"), nullable=True)
    
    estat = Column(Enum(EstatDraftEnum, name="estat_draft", native_enum=False), default=EstatDraftEnum.esborrany)
    
    subject = Column(String(200))
    cos = Column(Text)
    
    generat_per_ia = Column(Boolean, default=True)
    prompt_utilitzat = Column(Text)
    variants_generades = Column(JSONB, default=[]) 
    variant_seleccionada = Column(Integer, default=0)
    
    editat_per_usuari = Column(Boolean, default=False)
    canvis_respecte_ia = Column(JSONB, default={})
    
    data_enviament = Column(DateTime(timezone=True), nullable=True)
    enviat_des_de = Column(String(100))
    email_enviat_id = Column(UUID(as_uuid=True), ForeignKey("emails_v2.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    municipi = relationship("MunicipiLifecycle", back_populates="email_drafts")
    contacte = relationship("ContacteV2")

class EmailSequenciaV2(Base):
    __tablename__ = "email_sequencies_v2"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis_lifecycle.id"), nullable=False)
    
    numero_email = Column(Integer, nullable=False)
    tipus_sequencia = Column(Enum(TipusSequenciaEnum, name="tipus_sequencia", native_enum=False), nullable=False)
    
    estat = Column(Enum(EstatSequenciaEnum, name="estat_sequencia", native_enum=False), default=EstatSequenciaEnum.pendent)
    
    data_programada = Column(DateTime(timezone=True))
    data_enviada = Column(DateTime(timezone=True), nullable=True)
    
    draft_id = Column(UUID(as_uuid=True), ForeignKey("email_drafts_v2.id"), nullable=True)
    
    obert = Column(Boolean, default=False)
    data_obertura = Column(DateTime(timezone=True), nullable=True)
    respost = Column(Boolean, default=False)
    
    seguent_accio = Column(String(50), nullable=True)
    
    municipi = relationship("MunicipiLifecycle", back_populates="sequencia_emails")
    draft = relationship("EmailDraftV2")

# --- Memòria i Patrons ---

class MemoriaMunicipi(Base):
    __tablename__ = "memoria_municipis"
    
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis_lifecycle.id"), primary_key=True)
    
    ganxos_exitosos = Column(JSONB, default=[])
    angles_fallits = Column(JSONB, default=[])
    moment_optimal = Column(JSONB, default={}) # {"dia": "dimecres", "hora": "16:00"}
    llenguatge_preferit = Column(JSONB, default=[])
    blockers_resolts = Column(JSONB, default=[])
    
    # Nivell 2: Memòria Tàctica (Resum setmanal generat per IA)
    resum_tactic = Column(Text)
    data_resum = Column(DateTime(timezone=True))
    
    data_actualitzacio = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PatroMunicipi(Base):
    __tablename__ = "patrons_municipis"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    rang_poblacio = Column(String(20)) # 'petit', 'mitja', 'gran'
    tipus_geografia = Column(Enum(GeografiaEnum, name="geografia_patro", native_enum=False))
    context_politic = Column(String(20)) # 'majoria', 'minoria', 'pacte'
    
    probabilitat_conversio = Column(Float, default=0.0)
    temps_mitja_cicle_dies = Column(Integer, default=0)
    etapa_bloqueig_frequent = Column(String(50))
    
    estrategia_recomanada = Column(Text)
    objeccions_frequents = Column(JSONB, default=[])
    casos_exit_referencia = Column(JSONB, default=[])
    
    cops_aplicat = Column(Integer, default=0)
    exitosos = Column(Integer, default=0)


class ActivitatsMunicipi(Base):
    __tablename__ = "activitats_municipi"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis_lifecycle.id"), nullable=False)
    contacte_id = Column(UUID(as_uuid=True), ForeignKey("contactes_v2.id"), nullable=True)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id"), nullable=True)
    
    tipus_activitat = Column(Enum(TipusActivitat, name="tipus_activitat", native_enum=False), nullable=False)
    data_activitat = Column(DateTime(timezone=True), server_default=func.now())
    
    contingut = Column(JSONB, default={})
    notes_comercial = Column(Text)
    generat_per_ia = Column(Boolean, default=False)
    etiquetes = Column(ARRAY(String), default=[])
    
    # Relacions
    municipi = relationship("MunicipiLifecycle", back_populates="activitats")
    contacte = relationship("ContacteV2")

class AgentMemoryV2(Base):
    __tablename__ = "agent_memories_v2"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis_lifecycle.id"), nullable=False)
    
    clau = Column(String(50), index=True) # e.g. 'por_qué_no_compran', 'preferencia_politica'
    valor = Column(Text)
    confidenca = Column(Float, default=1.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    municipi = relationship("MunicipiLifecycle", back_populates="agent_memories")

class TascaV2(Base):
    __tablename__ = "tasques_v2"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis_lifecycle.id"), nullable=False)
    
    titol = Column(String(200), nullable=False)
    descripcio = Column(Text)
    data_venciment = Column(DateTime)
    prioritat = Column(String(20), default="mitjana") # 'alta', 'mitjana', 'baixa'
    estat = Column(String(20), default="pendent") # 'pendent', 'completada'
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    municipi = relationship("MunicipiLifecycle", back_populates="tasques")
