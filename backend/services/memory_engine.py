from sqlalchemy.orm import Session
from models_v2 import MunicipiLifecycle, MemoriaMunicipi, EmailV2, SentimentEnum
from datetime import datetime, timezone

def update_municipi_memory(db: Session, municipi_id: str):
    """
    Actualitza la memòria d'un municipi agregant estadístiques de comunicacions.
    Actualitza els angles_exitosos/angles_fallits d'Emails, Trucades o Reunions de manera reactiva.
    """
    m = db.query(MunicipiLifecycle).filter(MunicipiLifecycle.id == municipi_id).first()
    if not m:
        return

    memoria = db.query(MemoriaMunicipi).filter(MemoriaMunicipi.municipi_id == m.id).first()
    if not memoria:
        memoria = MemoriaMunicipi(municipi_id=m.id, ganxos_exitosos=[], angles_fallits=[], moment_optimal={}, llenguatge_preferit=[], blockers_resolts=[])
        db.add(memoria)

    # 1. Update 'dies_etapa_actual'
    if m.historial_etapes and len(m.historial_etapes) > 0:
         # Obtenim l'últim registre d'etapa per calcular el temps transcorregut
         d_inici = m.historial_etapes[-1].get("data_inici")
         if d_inici:
              try:
                   d_inici_dt = datetime.fromisoformat(d_inici)
                   diff = datetime.now(timezone.utc) - d_inici_dt
                   m.dies_etapa_actual = max(0, diff.days)
              except Exception:
                   pass

    # 2. Extract angles from Successful Response Emails
    # We find Emails with Sentiment positive/neutral and extract ideas
    emails = db.query(EmailV2).filter(EmailV2.municipi_id == m.id, EmailV2.sentiment_resposta == SentimentEnum.positiu).all()
    ganxos = list(memoria.ganxos_exitosos) if memoria.ganxos_exitosos else []
    angles_f = list(memoria.angles_fallits) if memoria.angles_fallits else []

    for e in emails:
        # Example: look for keywords in emails to extract succesful hooks
        if "reunió" in e.cos.lower() or "demo" in e.cos.lower():
             if "Angle: Demo / Proposta" not in ganxos:
                  ganxos.append("Angle: Demo / Proposta")

    memoria.ganxos_exitosos = list(set(ganxos)) # Evitem duplicats
    memoria.angles_fallits = list(set(angles_f))

    # Commit
    memoria.data_actualitzacio = datetime.now()
    db.commit()
    return memoria
