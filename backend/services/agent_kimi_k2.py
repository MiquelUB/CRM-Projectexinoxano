import json
import os
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta

from .prompt_manager import prompt_manager
import models_v2
import models
import logging

logger = logging.getLogger(__name__)

class AgentKimiK2:
    def __init__(self, db: Session):
        self.db = db

    def _load_context(self, municipi_id: UUID, limit: int = 50) -> List[models_v2.ActivitatsMunicipi]:
        """Retorna el timeline complet d'activitats del municipi."""
        return self.db.query(models_v2.ActivitatsMunicipi)\
            .filter(models_v2.ActivitatsMunicipi.municipi_id == municipi_id)\
            .order_by(desc(models_v2.ActivitatsMunicipi.data_activitat))\
            .limit(limit)\
            .all()

    async def _call_llm(self, messages: List[Dict[str, str]], skill: str, temperature: float = 0.7, json_mode: bool = False, model: Optional[str] = None):
        """Wrapper per cridar a OpenRouter amb una configuració específica."""
        from .openrouter_client import call_openrouter
        model_to_use = model or "moonshotai/kimi-k2-thinking"
        return await call_openrouter(messages, model=model_to_use, temperature=temperature, json_mode=json_mode)

    async def analitzar_context(self, municipi_id: UUID) -> Dict[str, Any]:
        """Skill: Analitzar l'estat actual del municipi basat en el seu historial."""
        activitats = self._load_context(municipi_id)
        
        if not activitats:
            return {
                "ultim_contacte": None,
                "dies_silence": 0,
                "bloquejos": [],
                "sentiment": "neutre"
            }

        ultima_act = activitats[0]
        if ultima_act.data_activitat:
            dies_silenci = (datetime.now().date() - ultima_act.data_activitat.date()).days
            data_str = ultima_act.data_activitat.strftime("%Y-%m-%d")
        else:
            dies_silenci = 0
            data_str = None
        
        bloquejos = []
        # Regla: Silenci prolongat
        if dies_silenci > 15:
            bloquejos.append(f"Sense resposta des de fa {dies_silenci} dies")

        # Regla: Demo sense seguiment
        foie_demo = any(a.tipus_activitat == models_v2.TipusActivitat.reunio for a in activitats[:5])
        if foie_demo and dies_silenci > 7:
            bloquejos.append("Oportunitat freda: Demo realitzada fa més de 7 dies sense seguiment actiu")

        return {
            "ultim_contacte": {
                "tipus": ultima_act.tipus_activitat.value if hasattr(ultima_act.tipus_activitat, 'value') else ultima_act.tipus_activitat,
                "data": data_str,
                "notes": ultima_act.notes_comercial
            },
            "dies_silence": dies_silenci,
            "bloquejos": bloquejos,
            "sentiment": "positiu" if dies_silenci < 5 else "neutre"
        }

    async def recomanar_accio(self, municipi_id: UUID) -> Dict[str, Any]:
        """Skill: Recomanar la següent millor acció comercial."""
        context_data = await self.analitzar_context(municipi_id)
        municipi = self.db.query(models_v2.MunicipiLifecycle).get(municipi_id)
        
        system_prompt = prompt_manager.render_prompt("recomanar_accio", {
            "nom_municipi": municipi.nom,
            "etapa": municipi.etapa_actual
        })
        
        user_content = f"ESTAT ACTUAL:\n{json.dumps(context_data, indent=2)}\n\nRecomana la següent acció comercial en format JSON."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        response = await self._call_llm(messages, skill="recomanar_accio", json_mode=True)
        try:
            return json.loads(response["content"])
        except:
            return {"score": 50, "accio": "Revisar manualment", "rao": "Error processant recomanació de l'IA"}

    async def redactar_email(self, municipi_id: UUID, contacte_id: Optional[UUID], tipus: str) -> List[Dict[str, str]]:
        """Skill: Generar variants d'email personalitzat."""
        municipi = self.db.query(models_v2.MunicipiLifecycle).get(municipi_id)
        contacte = self.db.query(models_v2.ContacteV2).get(contacte_id) if contacte_id else None
        context_data = await self.analitzar_context(municipi_id)
        
        prompt_key = f"redactar_email.{tipus}"
        try:
            # Comprovem si la variant existeix al manager
            system_prompt = prompt_manager.get_prompt(prompt_key)
        except:
            # Fallback simple
            system_prompt = prompt_manager.get_prompt("redactar_email")

        # Generar 3 variants amb diferents temperatures
        variants = []
        temperatures = [0.5, 0.7, 0.9]
        
        user_content = f"Municipi: {municipi.nom}\nContacte: {contacte.nom if contacte else 'Alcalde/ssa'}\nContext: {json.dumps(context_data)}"
        
        for temp in temperatures:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
            res = await self._call_llm(messages, skill="redactar_email", temperature=temp, json_mode=True)
            try:
                variant_data = json.loads(res["content"])
                variants.append(variant_data)
            except:
                continue
                
        return variants

    async def xat(self, usuari_id: UUID, message: str, municipi_id: Optional[UUID] = None, model: str = "moonshotai/kimi-k2-thinking") -> Dict[str, Any]:
        """Skill: Xat interactiu amb context del municipi i memòria persistent."""
        # Recuperar o crear memòria (usant memory_engine si existeix o directament)
        from .memory_engine import memory_engine
        
        # Obtenir context del municipi si m_id
        context_str = ""
        context_str = ""
        if municipi_id:
            municipi = self.db.query(models_v2.MunicipiLifecycle).get(municipi_id)
            if municipi:
                context_data = await self.analitzar_context(municipi_id)
                # Integrar Memòria Jeràrquica
                h_memory = await memory_engine.build_hierarchical_context(self.db, municipi_id, [])
                context_str = f"CONTEXT MUNICIPI {municipi.nom}:\n{json.dumps(context_data)}\n\nMEMÒRIA ESTRATÈGICA:\n{h_memory}"
        else:
            # Context GLOBAL: Veure què ha passat al CRM darrerament (emails globals)
            try:
                from models import Email
                ultims_emails = self.db.query(Email).order_by(Email.data_email.desc()).limit(5).all()
                if ultims_emails:
                    e_list = "\n".join([f"- [{e.data_email}] {e.direccio} de {e.from_address}: {e.assumpte}" for e in ultims_emails])
                    context_str = f"CONTEXT GLOBAL CRM (Últims emails):\n{e_list}"
                else:
                    context_str = "CONTEXT GLOBAL: No hi ha emails recents al sistema."
            except Exception as e:
                logger.error(f"Error carregant context global: {e}")
                context_str = "CONTEXT GLOBAL: No s'ha pogut carregar la informació d'emails."

        # Usar render_prompt per incloure la personalitat base i el sistema de xat
        system_prompt = prompt_manager.render_prompt("xat_conversacional", {
            "nom_municipi": municipi.nom if (municipi_id and 'municipi' in locals() and municipi) else "Global",
            "etapa": municipi.etapa_actual if (municipi_id and 'municipi' in locals() and municipi) else "N/A"
        })
        
        # Recuperar historial des de la DB
        memory = await memory_engine.get_or_create_memory(self.db, usuari_id, municipi_id=municipi_id)
        history = memory.history or []
        
        messages = [{"role": "system", "content": f"{system_prompt}\n\n{context_str}"}]
        
        # Afegir historial recent (últims 10)
        for h in history[-10:]:
            messages.append(h)
            
        messages.append({"role": "user", "content": message})
        
        response = await self._call_llm(messages, skill="xat", model=model)
        
        # Actualitzar historial
        new_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": response["content"]}
        ]
        memory.history = new_history
        memory.updated_at = datetime.now()
        self.db.commit()
        
        # Detecció d'accions sugerides (<<< Acció >>>)
        accions = []
        if ">>>>" in response["content"] or ">>>" in response["content"]:
             # Lògica d'extracció...
             pass
            
        return {
            "response": response["content"],
            "accions_suggerides": accions,
            "model": response["model_usat"]
        }

    def detectar_blockers(self, municipi_id: UUID) -> List[Dict[str, Any]]:
        """Skill: Detectar problemes en el pipeline basat en regles de negoci."""
        activitats = self._load_context(municipi_id)
        blockers = []
        now = datetime.now()

        if not activitats:
            return blockers

        ultima_act = activitats[0]
        if ultima_act.data_activitat:
            dies_silenci = (now.date() - ultima_act.data_activitat.date()).days
        else:
            dies_silenci = 0

        # Regla 1: Més de 15 dies sense resposta després d'un email
        if dies_silenci > 15:
            blockers.append({
                "tipus": "silenci",
                "descripcio": f"Silenci prolongat detectat ({dies_silenci} dies)",
                "dies_actiu": dies_silenci,
                "severitat": "alta"
            })

        # Regla 2: Demo feta fa >7 dies sense seguiment
        has_demo = any(a.tipus_activitat == models_v2.TipusActivitat.reunio for a in activitats)
        if has_demo and dies_silenci > 7:
            blockers.append({
                "tipus": "demo_freda",
                "descripcio": "Oportunitat freda: Demo realitzada sense seguiment en 7 dies",
                "dies_actiu": dies_silenci,
                "severitat": "mitjana"
            })

        # Regla 3: Proposta enviada fa >30 dies sense tancament
        has_proposal = any("proposta" in (a.notes_comercial or "").lower() for a in activitats)
        if has_proposal and dies_silenci > 30:
            blockers.append({
                "tipus": "cicle_bloquejat",
                "descripcio": "Cicle bloquejat: Proposta sense tancament des de fa 30 dies",
                "dies_actiu": dies_silenci,
                "severitat": "alta"
            })

        # Regla 4: Contacte mencionat "CFO" o "interventor" (Blocker legal/financer)
        potential_legal = any(k in (a.notes_comercial or "").upper() for a in activitats for k in ["CFO", "INTERVENTOR", "JURIDIC", "CONTRACTACIO"])
        if potential_legal:
            blockers.append({
                "tipus": "blocker_legal",
                "descripcio": "Blocker legal/financer detectat a les notes",
                "dies_actiu": 0,
                "severitat": "mitjana"
            })

        return blockers
