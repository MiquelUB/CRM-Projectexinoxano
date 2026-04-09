import json
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from uuid import UUID

import models_v2 as m2
import models
from .agent_manager import kimi_agent
from .memory_engine import memory_engine

logger = logging.getLogger(__name__)

class AgentChatService:
    def __init__(self, db: Session):
        self.db = db

    async def get_or_create_memory(self, usuari_id: UUID, deal_id: Optional[UUID] = None, municipi_id: Optional[UUID] = None):
        """Recupera o crea una entrada a agent_memories per a aquest context."""
        query = self.db.query(models.AgentMemory).filter(models.AgentMemory.usuari_id == usuari_id)
        
        if deal_id:
            query = query.filter(models.AgentMemory.deal_id == deal_id)
        elif municipi_id:
            query = query.filter(models.AgentMemory.municipi_id == municipi_id)
        else:
            query = query.filter(models.AgentMemory.deal_id == None, models.AgentMemory.municipi_id == None)

        memory = query.first()
        
        if not memory:
            memory = models.AgentMemory(
                usuari_id=usuari_id,
                deal_id=deal_id,
                municipi_id=municipi_id,
                history=[],
                summary="Inici de la conversa."
            )
            self.db.add(memory)
            self.db.commit()
            self.db.refresh(memory)
        
        return memory

    async def build_system_context(self, deal_id: Optional[UUID] = None, municipi_id: Optional[UUID] = None, history: List[Dict] = []):
        """Construeix un prompt de sistema ric en dades reals del CRM usant el gestor central i memòria jeràrquica."""
        context = kimi_agent.get_skill_system_prompt("analitzar_context")
        
        # Injectar Memòria Jeràrquica (Nivell 1, 2 i 3)
        m_id = municipi_id
        if deal_id and not m_id:
             deal = self.db.query(models.Deal).filter(models.Deal.id == deal_id).first()
             if deal: m_id = deal.municipi_id
             
        if m_id:
            h_memory = await memory_engine.build_hierarchical_context(self.db, m_id, history)
            context += f"\n{h_memory}\n"
        
        context += "\n\nREGLA CRÍTICA D'ANÀLISI:\n"
        context += "Ets un assessor basat en dades DEL CRM. El teu diagnòstic s'ha de basar ÚNICAMENT en les interaccions que apareixen a sota. Està TOTALMENT PROHIBIT inventar dades."
        
        context += "\n\n--- DADES REALS DEL CRM PER A L'ANÀLISI ---\n"

        # Afegir context del Municipi (Lifecycle + Memòria)
        m_id = municipi_id
        deal = None
        
        if not deal_id and not municipi_id:
            context += "\n[ALERTA: ACTUALMENT NO HI HA CAP DEAL NI MUNICIPI SELECCIONAT. Respon de manera general i demana concontext de treball.]\n"
        else:
            context += f"\n[CONTEXT ACTIU: {'Deal' if deal_id else 'Municipi'}]\n"

        if deal_id:
            deal = self.db.query(models.Deal).filter(models.Deal.id == deal_id).first()
            if deal:
                m_id = deal.municipi_id if not m_id else m_id
                context += f"CONTEXT DEL DEAL ACTUAL:\n- Títol: {deal.titol}\n- Etapa: {deal.etapa}\n- Valor: {deal.valor_setup}€ + {deal.valor_llicencia}€/any\n"
                if deal.proper_pas:
                    context += f"- Proper pas previst: {deal.proper_pas}\n"
                context += "\n"

        # Timeline Universal (Nova font de veritat)
        if m_id:
            activitats = self.db.query(m2.ActivitatsMunicipi).filter(m2.ActivitatsMunicipi.municipi_id == m_id).order_by(m2.ActivitatsMunicipi.data_activitat.desc()).limit(15).all()
            if activitats:
                context += "TIMELINE UNIVERSAL DEL MUNICIPI (Últimes interaccions):\n"
                for a in activitats:
                    data_str = a.data_activitat.strftime('%Y-%m-%d %H:%M') if a.data_activitat else 'Data desconeguda'
                    tipus = a.tipus_activitat.value if hasattr(a.tipus_activitat, 'value') else a.tipus_activitat
                    context += f"- [{data_str}] {tipus.upper()}: {a.notes_comercial or 'Sense notes'}\n"
                    # Afegir detalls rellevants del JSONB si cal
                    if a.contingut and tipus in ['trucada', 'reunio']:
                        resum = a.contingut.get('resum_ia') or a.contingut.get('tipus')
                        if resum:
                            context += f"  (Dades extra: {resum})\n"
                context += "\n"

        if m_id:
            # Intentar buscar a Lifecycle (V2) o Municipi (V1)
            m_life = self.db.query(m2.MunicipiLifecycle).filter(m2.MunicipiLifecycle.id == m_id).first()
            m_old = self.db.query(models.Municipi).filter(models.Municipi.id == m_id).first()
            m_memo = self.db.query(m2.MemoriaMunicipi).filter(m2.MemoriaMunicipi.municipi_id == m_id).first()
            
            if m_life:
                context += f"DADES DEL MUNICIPI ({m_life.nom}):\n"
                context += f"- Població: {m_life.poblacio or 'No consta'}\n"
                context += f"- Etapa Funnel: {m_life.etapa_actual.value if hasattr(m_life.etapa_actual, 'value') else m_life.etapa_actual}\n"
                context += f"- Temperatura: {m_life.temperatura.value if hasattr(m_life.temperatura, 'value') else m_life.temperatura}\n"
                context += f"- Angle personalitzacio: {m_life.angle_personalitzacio or 'Estàndard'}\n"
            elif m_old:
                context += f"DADES DEL MUNICIPI ({m_old.nom}):\n"
                context += f"- Població: {m_old.poblacio or 'No consta'}\n"
                context += f"- Tipus: {m_old.tipus}\n"
            
            if m_memo:
                context += f"\nMEMÒRIA ESTRATÈGICA DEL TERRITORI:\n"
                context += f"- Ganxos que han funcionat: {m_memo.ganxos_exitosos}\n"
                context += f"- Angles que han fallat: {m_memo.angles_fallits}\n"
                context += f"- To preferit: {m_memo.llenguatge_preferit}\n"

        context += "\nRecorda: Ets en Kimi. Sigues executiu i tàctic. Usa les dades reals de dalt per fonamentar el teu diagnòstic."
        return context

    async def chat(self, usuari_id: UUID, message: str, deal_id: Optional[UUID] = None, municipi_id: Optional[UUID] = None, model: str = "google/gemini-2.0-flash-001"):
        """Executa una interacció de xat i guarda la memòria."""
        memory = await self.get_or_create_memory(usuari_id, deal_id, municipi_id)
        history = memory.history or []
        system_prompt = await self.build_system_context(deal_id, municipi_id, history)

        # Preparar missatges (Context + Memòria + Nou Missatge)
        messages = [{"role": "system", "content": system_prompt}]
        
        # Afegir resum si n'hi ha
        if memory.summary:
            messages.append({"role": "system", "content": f"RESUM DE LA CONVERSA PRÈVIA: {memory.summary}"})
        
        # Afegir últims 10 missatges de l'historial
        history = memory.history or []
        for h in history[-10:]:
            messages.append(h)
        
        # Afegir el nou missatge
        messages.append({"role": "user", "content": message})

        # Crida a l'IA (Kimi K2 / Deepseek / Claude)
        response = await call_openrouter(messages, model=model)
        
        # Actualitzar historial
        new_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": response["content"]}
        ]
        
        memory.history = new_history
        memory.updated_at = datetime.now(timezone.utc)
        
        # Opcional: Generar nou resum si l'historial és llarg (> 20 msgs)
        if len(new_history) > 20:
            summary_prompt = messages + [{"role": "user", "content": "Genera un resum molt breu (2 línies) d'aquesta conversa per a la teva memòria futura."}]
            sum_res = await call_openrouter(summary_prompt, model=model)
            memory.summary = sum_res["content"]

        self.db.commit()
        
        # Extreure accions suggerides (línies que comencen amb >>>)
        accions = []
        lines = response["content"].splitlines()
        clean_content = []
        for line in lines:
            if line.strip().startswith(">>>"):
                accio_text = line.replace(">>>", "").strip()
                if accio_text:
                    accions.append(accio_text)
            else:
                clean_content.append(line)
        
        final_content = "\n".join(clean_content).strip()

        return {
            "response": final_content,
            "accions_suggerides": accions,
            "model": response["model_usat"],
            "history_count": len(new_history)
        }
