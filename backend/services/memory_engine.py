
import uuid
import logging
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
import models
from .agent_manager import kimi_agent
import json
from uuid import UUID

logger = logging.getLogger(__name__)

class MemoryEngine:
    async def get_or_create_memory(self, db: Session, usuari_id: UUID, municipi_id: Optional[UUID] = None) -> models.AgentMemory:
        try:
            query = db.query(models.AgentMemory).filter(models.AgentMemory.usuari_id == usuari_id)
            if municipi_id:
                query = query.filter(models.AgentMemory.municipi_id == municipi_id)
            else:
                query = query.filter(models.AgentMemory.municipi_id == None)
            
            memory = query.order_by(models.AgentMemory.updated_at.desc()).first()
        except Exception as e:
            db.rollback()
            logger.warning(f"Error llegint memòria: {e}")
            memory = None
            
        if not memory:
            try:
                memory = models.AgentMemory(
                    id=uuid.uuid4(), usuari_id=usuari_id, municipi_id=municipi_id, history=[], summary=""
                )
                db.add(memory)
                db.commit()
                db.refresh(memory)
            except Exception as e:
                db.rollback()
                logger.error(f"Error creant memòria: {e}")
                memory = models.AgentMemory(history=[], summary="", usuari_id=usuari_id, municipi_id=municipi_id)
            
        return memory

    @staticmethod
    async def get_tactical_summary(db: Session, municipi_id: Any) -> str:
        # Busquem la memòria compartida o de l'usuari admin per a aquest municipi
        mem = db.query(models.AgentMemory).filter(models.AgentMemory.municipi_id == municipi_id).order_by(models.AgentMemory.updated_at.desc()).first()
        
        if not mem or not mem.summary or (mem.updated_at and (datetime.now(timezone.utc) - mem.updated_at.replace(tzinfo=timezone.utc)).days > 3):
            activitats = db.query(models.Activitat)\
                .filter(models.Activitat.municipi_id == municipi_id)\
                .order_by(models.Activitat.data_activitat.desc())\
                .limit(10).all()
            
            if not activitats:
                return "Sense activitat recent registrada."
            
            timeline_str = ""
            for a in activitats:
                data_act = a.data_activitat.strftime('%Y-%m-%d') if a.data_activitat else "S/D"
                timeline_str += f"- [{data_act}] {a.tipus_activitat}: {a.notes_comercial or ''}\n"
            
            try:
                res = await kimi_agent.call_skill("generar_resum_tactic", timeline_str)
                resum = res["content"].strip()
                
                if not mem:
                    mem = models.AgentMemory(municipi_id=municipi_id, summary=resum)
                    db.add(mem)
                else:
                    mem.summary = resum
                    mem.updated_at = datetime.now(timezone.utc)
                
                db.commit()
                return resum
            except Exception as e:
                logger.error(f"Error generant resum tactic: {e}")
                return mem.summary if mem else "No s'ha pogut generar el resum."
        
        return mem.summary

    @classmethod
    async def build_hierarchical_context(cls, db: Session, municipi_id: Any, session_history: List[Dict] = []) -> str:
        municipi = db.query(models.Municipi).filter(models.Municipi.id == municipi_id).first()
        if not municipi:
            return "No hi ha context disponible."

        tactical = await cls.get_tactical_summary(db, municipi_id)
        
        session_str = "Sense historial previ."
        if session_history:
            last_msgs = session_history[-3:]
            session_str = "\n".join([f"{m['role'].upper()}: {m['content'][:100]}..." for m in last_msgs])

        hierarchical_prompt = f"""
SISTEMA DE MEMÒRIA:
[SESSIÓ] {session_str}
[TÀCTIC] ({municipi.nom}): {tactical}
"""
        return hierarchical_prompt

memory_engine = MemoryEngine()
