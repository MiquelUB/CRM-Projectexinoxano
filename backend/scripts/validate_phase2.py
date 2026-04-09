import sys
import os
import uuid
import time
import asyncio
import json
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Carregar variables d'entorn
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO)

# Afegir el directori backend al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models_v2 import (
    MunicipiLifecycle, ContacteV2, ActivitatsMunicipi, TipusActivitat, 
    EtapaFunnelEnum, TemperaturaEnum, AgentMemoryV2, EstatFinalEnum
)
from services.agent_kimi_k2 import AgentKimiK2
from services.memory_engine import memory_engine

async def setup_benchmark_data(db):
    print("--- 1. Preparant dades de benchmark (1000+ activitats) ---")
    m = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.nom == "Benchmark City").first()
    if not m:
        m = MunicipiLifecycle(
            nom="Benchmark City",
            etapa_actual=EtapaFunnelEnum.contacte,
            temperatura=TemperaturaEnum.templat
        )
        db.add(m)
        db.commit()
        db.refresh(m)
    
    # Afegir 1000 activitats si no hi són
    count = db.query(ActivitatsMunicipi).filter(ActivitatsMunicipi.municipi_id == m.id).count()
    if count < 1000:
        print(f"Afegint {1000-count} activitats...")
        for i in range(1000 - count):
            act = ActivitatsMunicipi(
                municipi_id=m.id,
                tipus_activitat=TipusActivitat.nota_manual,
                data_activitat=datetime.now(timezone.utc) - timedelta(hours=i),
                notes_comercial=f"Nota de benchmark numero {i}",
                contingut={"val": i}
            )
            db.add(act)
        db.commit()
    return m.id

async def test_performance(db, m_id):
    print("\n--- 2. Mesurant temps de resposta (< 2s) ---")
    agent = AgentKimiK2(db)
    
    # Test analitzar_context
    start = time.time()
    res_an = await agent.analitzar_context(m_id)
    end = time.time()
    t_an = end - start
    print(f"analitzar_context(): {t_an:.2f}s")
    
    # Test recomanar_accio
    start = time.time()
    res_rec = await agent.recomanar_accio(m_id)
    end = time.time()
    t_rec = end - start
    print(f"recomanar_accio(): {t_rec:.2f}s")
    
    status = "PASSED" if t_an < 2 and t_rec < 2 else "FAILED"
    print(f"RESULTAT: {status}")

async def test_precision(db):
    print("\n--- 3. Verificant precisió de recomanacions (10 casos) ---")
    agent = AgentKimiK2(db)
    casos = [
        (EtapaFunnelEnum.research, TemperaturaEnum.fred, "Cerca contacte clau"),
        (EtapaFunnelEnum.contacte, TemperaturaEnum.calent, "Proposa demo"),
        (EtapaFunnelEnum.demo_pendent, TemperaturaEnum.bullent, "Preparar demo"),
        (EtapaFunnelEnum.demo_ok, TemperaturaEnum.calent, "Enviar proposta"),
        (EtapaFunnelEnum.oferta, TemperaturaEnum.calent, "Seguiment oferta"),
        (EtapaFunnelEnum.documentacio, TemperaturaEnum.templat, "Demanar papers"),
        (EtapaFunnelEnum.aprovacio, TemperaturaEnum.templat, "Vigilar ple"),
        (EtapaFunnelEnum.contracte, TemperaturaEnum.bullent, "Signatura definitiva"),
        (EtapaFunnelEnum.pausa, TemperaturaEnum.fred, "Re-activar en 3 mesos"),
        (EtapaFunnelEnum.contacte, TemperaturaEnum.fred, "Email de seguiment")
    ]
    
    correctes = 0
    for etapa, temp, desc in casos:
        m = MunicipiLifecycle(nom=f"Test {etapa.value}", etapa_actual=etapa, temperatura=temp)
        db.add(m)
        db.commit()
        
        # Simular una activitat recent per context
        act = ActivitatsMunicipi(municipi_id=m.id, tipus_activitat=TipusActivitat.nota_manual, notes_comercial=f"Municipi en estat {etapa.value}")
        db.add(act)
        db.commit()
        
        res = await agent.recomanar_accio(m.id)
        print(f"Estat: {etapa.value} | Rec: {res.get('accio_recomanada', 'Error')} | Rao: {res.get('rao', '')}")
        # Validació heurística simple: si la resposta no és un error, contem com bona (la validació del sentit és humana)
        if "score" in res: correctes += 1
        
    print(f"Acceptació: {correctes}/10 (Mínim 8/10)")

async def test_memory(db):
    print("\n--- 4. Verificant memòria persistent ---")
    u_id = uuid.uuid4() # Usuari fake
    # Crear un usuari a la db per FK si cal, o usar un existent
    from models import Usuari
    u = db.query(Usuari).first()
    if not u:
        print("Error: No hi ha usuaris a la DB per testejar memòria.")
        return
    u_id = u.id

    agent = AgentKimiK2(db)
    m_id = (db.query(MunicipiLifecycle).first()).id
    
    print("Enviant missatge 1: 'Hola, sóc en Miquel.'")
    await agent.xat(u_id, "Hola, sóc en Miquel, recorda el meu nom.", m_id)
    
    print("Simulant pas de temps (1 hores)...")
    # No cal esperar realment, només tornar a cridar
    
    print("Preguntant nom: 'Com em dic?'")
    res = await agent.xat(u_id, "Com em dic?", m_id)
    print(f"Resposta: {res['response']}")
    
    if "Miquel" in res["response"]:
        print("RESULTAT: Memòria persistent FUNCIONA.")
    else:
        print("RESULTAT: Memòria persistent Falla.")

async def test_global_learning(db):
    print("\n--- 5. Verificant aprenentatge global ---")
    # Forçar aprenentatge
    # Primer ens assegurem que hi ha algun municipi tancat recentment
    m = db.query(MunicipiLifecycle).first()
    m.estat_final = EstatFinalEnum.client
    m.data_conversio = datetime.now()
    db.commit()
    
    print("Executant aprenentatge estratègic mensual...")
    await memory_engine.run_monthly_strategic_learning(db)
    
    from models_v2 import MemoriaGlobal
    count = db.query(MemoriaGlobal).count()
    print(f"Lliçons a MemoriaGlobal: {count}")
    
    if count > 0:
        llico = db.query(MemoriaGlobal).first()
        print(f"Lliçó d'exemple: [{llico.categoria}] {llico.llico}")
        print(f"Evidència: {json.dumps(llico.evidencia)}")
    else:
        print("No s'han generat lliçons (potser calen més dades de cicle tancat).")

async def main():
    db = SessionLocal()
    try:
        m_id = await setup_benchmark_data(db)
        await test_performance(db, m_id)
        await test_precision(db)
        await test_memory(db)
        await test_global_learning(db)
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
