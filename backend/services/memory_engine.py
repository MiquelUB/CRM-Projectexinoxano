from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import models_v2 as m2
from .agent_manager import kimi_agent

class MemoryEngine:
    """
    Motor de Memòria Jeràrquica per a l'Agent Kimi K2.
    Gestiona la recuperació i síntesi de context en 3 nivells.
    """

    @staticmethod
    async def get_tactical_summary(db: Session, municipi_id: Any) -> str:
        """
        Nivell 2 (Tàctic): Recupera el resum d'activitat recent.
        Si el resum té més de 3 dies, en genera un de nou.
        """
        mem = db.query(m2.MemoriaMunicipi).filter(m2.MemoriaMunicipi.municipi_id == municipi_id).first()
        
        # Si no hi ha memòria o és vella, regenerar
        if not mem or not mem.resum_tactic or (mem.data_resum and (datetime.utcnow() - mem.data_resum).days > 3):
            # Obtenir darreres activitats
            activitats = db.query(m2.ActivitatsMunicipi)\
                .filter(m2.ActivitatsMunicipi.municipi_id == municipi_id)\
                .order_by(m2.ActivitatsMunicipi.data_activitat.desc())\
                .limit(10).all()
            
            if not activitats:
                return "Sense activitat recent registrada per a aquest municipi."
            
            # Construir context per a la IA
            timeline_str = ""
            for a in activitats:
                timeline_str += f"- [{a.data_activitat.strftime('%Y-%m-%d')}] {a.tipus_activitat.value}: {a.notes_comercial or ''}\n"
            
            # Cridar a la skill de síntesi
            try:
                res = await kimi_agent.call_skill("generar_resum_tactic", timeline_str)
                resum = res["content"].strip()
                
                if not mem:
                    mem = m2.MemoriaMunicipi(municipi_id=municipi_id, resum_tactic=resum, data_resum=datetime.utcnow())
                    db.add(mem)
                else:
                    mem.resum_tactic = resum
                    mem.data_resum = datetime.utcnow()
                
                db.commit()
                return resum
            except Exception:
                return mem.resum_tactic if mem else "No s'ha pogut generar el resum tactic."
        
        return mem.resum_tactic

    @staticmethod
    def get_strategic_patterns(db: Session, municipi: m2.MunicipiLifecycle) -> List[str]:
        """
        Nivell 3 (Estratègic): Busca patrons globals rellevants.
        """
        # Cercar per rang de població i geografia
        poblacio_rang = 'petit'
        if municipi.poblacio:
            if municipi.poblacio > 20000: poblacio_rang = 'gran'
            elif municipi.poblacio > 5000: poblacio_rang = 'mitja'
            
        patrons = db.query(m2.PatroMunicipi).filter(
            (m2.PatroMunicipi.rang_poblacio == poblacio_rang) | 
            (m2.PatroMunicipi.tipus_geografia == municipi.geografia)
        ).limit(2).all()
        
        return [p.estrategia_recomanada for p in patrons if p.estrategia_recomanada]

    @classmethod
    async def build_hierarchical_context(cls, db: Session, municipi_id: Any, session_history: List[Dict] = []) -> str:
        """
        Uneix els 3 nivells de memòria en un bloc de context per al prompt del xat.
        """
        municipi = db.query(m2.MunicipiLifecycle).filter(m2.MunicipiLifecycle.id == municipi_id).first()
        if not municipi:
            return "No hi ha context de municipi disponible."

        # 1. Nivell 2 (Tàctic)
        tactical = await cls.get_tactical_summary(db, municipi_id)
        
        # 2. Nivell 3 (Estratègic)
        strategic = cls.get_strategic_patterns(db, municipi)
        strategic_str = "\n".join([f"- {s}" for s in strategic]) if strategic else "No hi ha patrons globals coneguts encara."
        
        # 3. Nivell 1 (Sessió) - resum breu de l'historial
        session_str = "Sense historial previ en aquesta sessió."
        if session_history:
            last_msgs = session_history[-3:]
            session_str = "\n".join([f"{m['role'].upper()}: {m['content'][:100]}..." for m in last_msgs])

        hierarchical_prompt = f"""
SISTEMA DE MEMÒRIA JERÀRQUICA:

[NIVELL 1 - SESSIÓ (Xat Actual)]
{session_str}

[NIVELL 2 - TÀCTIC (Municipi: {municipi.nom})]
{tactical}

[NIVELL 3 - ESTRATÈGIC (Casos similars)]
{strategic_str}
"""
        return hierarchical_prompt

memory_engine = MemoryEngine()
