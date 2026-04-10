import uuid
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import models_v2 as m2
from .agent_manager import kimi_agent
import json
from uuid import UUID

class MemoryEngine:
    """
    Motor de Memòria Jeràrquica per a l'Agent Kimi K2.
    Gestiona la recuperació i síntesi de context en 3 nivells.
    """

    async def get_or_create_memory(self, db: Session, usuari_id: UUID, municipi_id: Optional[UUID] = None) -> m2.AgentMemoryV2:
        """Recupera o crea una instància de memòria per a l'usuari i context."""
        query = db.query(m2.AgentMemoryV2).filter(
            m2.AgentMemoryV2.usuari_id == usuari_id
        )
        if municipi_id:
            query = query.filter(m2.AgentMemoryV2.municipi_id == municipi_id)
        else:
            query = query.filter(m2.AgentMemoryV2.municipi_id == None)
        
        # Agafem la més recent
        memory = query.order_by(m2.AgentMemoryV2.updated_at.desc()).first()
        
        if not memory:
            memory = m2.AgentMemoryV2(
                id=uuid.uuid4(),
                usuari_id=usuari_id,
                municipi_id=municipi_id,
                history=[],
                summary=""
            )
            db.add(memory)
            db.commit()
            db.refresh(memory)
            
        return memory

    @classmethod
    async def _get_full_timeline(cls, db: Session, target_id: str) -> List[Dict[str, Any]]:
        """Recupera totes les activitats d'un municipi per a l'anàlisi estratègica."""
        activitats = db.query(m2.ActivitatsMunicipi).filter(
            m2.ActivitatsMunicipi.municipi_id == target_id
        ).order_by(m2.ActivitatsMunicipi.data_activitat.asc()).all()
        
        return [
            {
                "data": a.data_activitat.isoformat() if a.data_activitat else "",
                "tipus": a.tipus_activitat.value if hasattr(a.tipus_activitat, 'value') else str(a.tipus_activitat),
                "contingut": getattr(a, 'contingut', ''),
                "notes": a.notes_comercial
            } for a in activitats
        ]

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

    @classmethod
    async def run_weekly_aggregation(cls, db: Session):
        """
        Executa l'agregació de Nivell 2 per a tots els municipis.
        Cronjob executat cada dilluns.
        """
        from models_v2 import MunicipiLifecycle, ActivitatsMunicipi, TipusActivitat
        from datetime import datetime, timedelta
        
        avui = datetime.utcnow()
        setmana_passada = avui - timedelta(days=7)
        setmana_id = avui.strftime("%Y-W%W")
        
        municipis = db.query(MunicipiLifecycle).all()
        for m in municipis:
            # Comptar activitats de la setmana passada
            activitats = db.query(ActivitatsMunicipi).filter(
                ActivitatsMunicipi.municipi_id == m.id,
                ActivitatsMunicipi.data_activitat >= setmana_passada
            ).all()
            
            if not activitats:
                continue
                
            stats = {
                "setmana": setmana_id,
                "activitats_totals": len(activitats),
                "emails_enviats": len([a for a in activitats if a.tipus_activitat == TipusActivitat.email_enviat]),
                "emails_rebuts": len([a for a in activitats if a.tipus_activitat == TipusActivitat.email_rebut]),
                "trucades": len([a for a in activitats if a.tipus_activitat == TipusActivitat.trucada]),
                "reunions": len([a for a in activitats if a.tipus_activitat == TipusActivitat.reunio]),
                "sentiment_general": "neutre", # Es podria calcular amb LLM
                "highlights": []
            }
            
            # Cridar LLM per a highlights
            if stats["activitats_totals"] > 0:
                timeline_str = "\n".join([f"- {a.tipus_activitat.value}: {a.notes_comercial or ''}" for a in activitats])
                try:
                    prompt = f"Resumeix les activitats de la setmana pel municipi {m.nom} en 2-3 punts clau:\n{timeline_str}"
                    res = await kimi_agent.call_skill("generar_highlights", prompt)
                    stats["highlights"] = [line.strip("- ").strip() for line in res["content"].splitlines() if line.strip()]
                except Exception as e:
                    logger.error(f"Error generant highlights per {m.nom}: {e}")

            # Guardar a resum_setmanal
            mem = db.query(m2.MemoriaMunicipi).filter(m2.MemoriaMunicipi.municipi_id == m.id).first()
            if not mem:
                mem = m2.MemoriaMunicipi(municipi_id=m.id, resum_setmanal=stats)
                db.add(mem)
            else:
                mem.resum_setmanal = stats
            
        db.commit()

    @classmethod
    async def run_monthly_strategic_learning(cls, db: Session):
        """
        Executa l'aprenentatge de Nivell 3 (Estratègic).
        Analitza conversions i pèrdues de l'últim mes.
        """
        from models_v2 import MunicipiLifecycle, EstatFinalEnum, MemoriaGlobal
        from datetime import datetime, timedelta
        
        avui = datetime.utcnow()
        mes_passat = avui - timedelta(days=30)
        
        # Municipis tancats (positiu o negatiu) aquest mes
        municipis_tancats = db.query(MunicipiLifecycle).filter(
            MunicipiLifecycle.estat_final.isnot(None),
            MunicipiLifecycle.data_conversio >= mes_passat
        ).all()
        
        if not municipis_tancats:
            logger.info("No hi ha municipis tancats aquest mes per analitzar.")
            return

        for m in municipis_tancats:
            # Carregar context complet de tancament
            timeline = await cls._get_full_timeline(db, str(m.id))
            status = "ÈXIT" if m.estat_final == EstatFinalEnum.client else "FRACÀS"
            
            prompt = f"Analitza el següent timeline de tancament de {m.nom} ({status}):\n{timeline}\nExtrau una lliçó estratègica."
            
            try:
                res = await kimi_agent.call_skill("aprenentatge_estrategic", prompt)
                import json
                llico_data = json.loads(res["content"])
                
                # Afegir a MemoriaGlobal
                m_global = MemoriaGlobal(
                    categoria=llico_data["categoria"],
                    llico=llico_data["llico"],
                    confianca=llico_data["confianca"],
                    evidencia={"municipi_id": str(m.id), "nom": m.nom, "estat": status}
                )
                db.add(m_global)
            except Exception as e:
                logger.error(f"Error aprenentatge estratègic per {m.nom}: {e}")
        
        db.commit()
        logger.info(f"Aprenentatge mensual completat per {len(municipis_tancats)} municipis.")

memory_engine = MemoryEngine()
