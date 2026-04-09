import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
import uuid
from datetime import datetime

# Setup test DB (SQLite for tests)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_activitats.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    # Crear un municipi de prova
    db = TestingSessionLocal()
    from models_v2 import MunicipiLifecycle, EtapaFunnelEnum, TemperaturaEnum
    m_id = uuid.UUID("98b50e2d-dc99-43ef-b387-052637738f61")
    if not db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == m_id).first():
        m = MunicipiLifecycle(
            id=m_id,
            nom="Test Municipi",
            etapa_actual=EtapaFunnelEnum.research,
            temperatura=TemperaturaEnum.fred
        )
        db.add(m)
        db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

# TEST 1: Crear activitat nota_manual
def test_create_nota_manual():
    response = client.post("/api/v2/activitats/", json={
        "municipi_id": "98b50e2d-dc99-43ef-b387-052637738f61",
        "tipus_activitat": "nota_manual",
        "notes_comercial": "Test nota manual",
        "generat_per_ia": False
    })
    assert response.status_code == 201
    data = response.json()
    assert data["tipus_activitat"] == "nota_manual"
    assert data["notes_comercial"] == "Test nota manual"
    assert "id" in data
    assert "created_at" in data

# TEST 2: Crear activitat email_enviat amb JSONB
def test_create_email_activitat():
    contingut = {"assumpte": "Test", "to": "test@example.com"}
    response = client.post("/api/v2/activitats/", json={
        "municipi_id": "98b50e2d-dc99-43ef-b387-052637738f61",
        "tipus_activitat": "email_enviat",
        "contingut": contingut
    })
    assert response.status_code == 201
    data = response.json()
    assert data["contingut"] == contingut
    # Verificar recuperació
    act_id = data["id"]
    get_resp = client.get(f"/api/v2/activitats/municipi/98b50e2d-dc99-43ef-b387-052637738f61")
    assert any(item["id"] == act_id for item in get_resp.json()["items"])

# TEST 3: Llistar amb paginació
def test_pagination():
    # Crear 25 activitats
    for i in range(25):
        client.post("/api/v2/activitats/", json={
            "municipi_id": "98b50e2d-dc99-43ef-b387-052637738f61",
            "tipus_activitat": "trucada",
            "notes_comercial": f"Activitat {i}"
        })
    
    response = client.get("/api/v2/activitats/municipi/98b50e2d-dc99-43ef-b387-052637738f61?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] == 25
    assert data["pages"] == 3

# TEST 4: Filtrar per tipus
def test_filter_by_type():
    # 3 emails, 2 trucades
    for _ in range(3):
        client.post("/api/v2/activitats/", json={
            "municipi_id": "98b50e2d-dc99-43ef-b387-052637738f61",
            "tipus_activitat": "email_enviat"
        })
    for _ in range(2):
        client.post("/api/v2/activitats/", json={
            "municipi_id": "98b50e2d-dc99-43ef-b387-052637738f61",
            "tipus_activitat": "trucada"
        })
    
    response = client.get("/api/v2/activitats/municipi/98b50e2d-dc99-43ef-b387-052637738f61?tipus_activitat=email_enviat")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 3
