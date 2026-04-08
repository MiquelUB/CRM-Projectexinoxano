import uuid
from sqlalchemy import Column, String, Boolean, Integer, Text, Numeric, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from database import Base

class AgentMemory(Base):
    __tablename__ = "agent_memories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuari_id = Column(UUID(as_uuid=True), ForeignKey("usuaris.id"), nullable=False)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id"), nullable=True)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis.id"), nullable=True)
    history = Column(JSONB, default=[])
    summary = Column(Text)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    usuari = relationship("Usuari", backref="agent_memories")
    deal = relationship("Deal", backref="agent_memories")
    municipi = relationship("Municipi", backref="agent_memories")

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

class Municipi(Base):
    __tablename__ = "municipis"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String(200), nullable=False)
    tipus = Column(String(50), nullable=False) # 'ajuntament' | 'diputacio' | 'consell_comarcal'
    provincia = Column(String(100))
    poblacio = Column(String(255))
    codi_postal = Column(String(10), nullable=True)
    web = Column(String(255))
    telefon = Column(String(50))
    adreca = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    contactes = relationship("Contacte", back_populates="municipi", cascade="all, delete-orphan")
    deals = relationship("Deal", back_populates="municipi", cascade="all, delete-orphan")

class Contacte(Base):
    __tablename__ = "contactes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis.id"), nullable=False)
    nom = Column(String(200), nullable=False)
    carrec = Column(String(200))
    email = Column(String(255))
    telefon = Column(String(50))
    linkedin = Column(String(255))
    notes_humanes = Column(Text)
    actiu = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    municipi = relationship("Municipi", back_populates="contactes", lazy="joined")
    deals = relationship("Deal", back_populates="contacte")

class Deal(Base):
    __tablename__ = "deals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis.id"), nullable=False)
    contacte_id = Column(UUID(as_uuid=True), ForeignKey("contactes.id"), nullable=True)
    titol = Column(String(300), nullable=False)
    etapa = Column(String(50), default="prospecte", nullable=False) 
    valor_setup = Column(Numeric(10, 2), default=0)
    valor_llicencia = Column(Numeric(10, 2), default=0)
    prioritat = Column(String(20), default="mitjana") # 'alta' | 'mitjana' | 'baixa'
    notes_humanes = Column(Text)
    proper_pas = Column(Text)
    data_seguiment = Column(Date)
    data_tancament_prev = Column(Date)
    data_tancament_real = Column(Date)
    motiu_perdua = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    municipi = relationship("Municipi", back_populates="deals", lazy="joined")
    contacte = relationship("Contacte", back_populates="deals", lazy="joined")
    activitats = relationship("DealActivitat", back_populates="deal", cascade="all, delete-orphan")

class DealActivitat(Base):
    __tablename__ = "deal_activitats"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id"), nullable=False)
    tipus = Column(String(50), nullable=False) # 'canvi_etapa' | 'nota' | 'email_enviat' | 'email_rebut'
    descripcio = Column(Text, nullable=False)
    valor_anterior = Column(String(255), nullable=True)
    valor_nou = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    deal = relationship("Deal", back_populates="activitats")

class Email(Base):
    __tablename__ = "emails"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id"), nullable=True)
    contacte_id = Column(UUID(as_uuid=True), ForeignKey("contactes.id"), nullable=True)
    campanya_id = Column(UUID(as_uuid=True), nullable=True) 
    from_address = Column(String(255), nullable=False)
    to_address = Column(String(255), nullable=False)
    assumpte = Column(String(500), nullable=False)
    cos = Column(Text)
    direccio = Column(String(3), nullable=False) # 'IN' | 'OUT'
    llegit = Column(Boolean, default=False)
    sincronitzat = Column(Boolean, default=False)
    message_id_extern = Column(String(500), unique=True, nullable=True)
    data_email = Column(DateTime(timezone=True), nullable=False)
    tracking_token = Column(String(100), unique=True, nullable=True)
    obert = Column(Boolean, default=False)
    data_obertura = Column(DateTime(timezone=True), nullable=True)
    nombre_obertures = Column(Integer, default=0)
    ip_obertura = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    deal = relationship("Deal", backref="emails")
    contacte = relationship("Contacte", backref="emails_rel")

class Llicencia(Base):
    __tablename__ = "llicencies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id"), nullable=False, unique=True)
    data_inici = Column(Date, nullable=False)
    data_renovacio = Column(Date, nullable=False)
    estat = Column(String(50), default="activa") # activa | suspesa | cancel·lada
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    deal = relationship("Deal", backref="llicencia", uselist=False)
    pagaments = relationship("Pagament", back_populates="llicencia", cascade="all, delete-orphan")

class Pagament(Base):
    __tablename__ = "pagaments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    llicencia_id = Column(UUID(as_uuid=True), ForeignKey("llicencies.id"), nullable=False)
    import_ = Column("import", Numeric(10, 2), nullable=False)
    tipus = Column(String(50), nullable=False) # setup_fee | llicencia_anual
    estat = Column(String(50), default="emes") # emes | confirmat | vencut | proper
    data_emisio = Column(Date, nullable=False)
    data_limit = Column(Date)
    data_confirmacio = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    llicencia = relationship("Llicencia", back_populates="pagaments")

class Tasca(Base):
    __tablename__ = "tasques"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id"), nullable=True)
    contacte_id = Column(UUID(as_uuid=True), ForeignKey("contactes.id"), nullable=True)
    municipi_id = Column(UUID(as_uuid=True), ForeignKey("municipis.id"), nullable=True)
    usuari_id = Column(UUID(as_uuid=True), ForeignKey("usuaris.id"), nullable=True)
    
    titol = Column(String(300), nullable=False)
    descripcio = Column(Text)
    data_venciment = Column(Date, nullable=False)
    tipus = Column(String(50), default="altre") # 'trucada' | 'email' | 'demo' | 'reunio' | 'altre'
    prioritat = Column(String(20), default="mitjana") # 'alta' | 'mitjana' | 'baixa'
    estat = Column(String(20), default="pendent") # 'pendent' | 'completada' | 'cancel·lada'
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    deal = relationship("Deal", backref="tasques")
    contacte = relationship("Contacte", backref="tasques")
    municipi = relationship("Municipi", backref="tasques")
    usuari = relationship("Usuari", backref="tasques")
