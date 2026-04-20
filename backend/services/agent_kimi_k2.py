
import json
import os
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta, timezone

from .prompt_manager import prompt_manager
from .memory_engine import memory_engine
import models
import logging

logger = logging.getLogger(__name__)

class AgentKimiK2:
    def __init__(self, db: Session):
        self.db = db

    def _load_context(self, municipi_id: UUID, limit: int = 50) -> List[Dict[str, Any]]:
        """Retorna el timeline complet d'activitats del municipi usant el model unificat."""
        timeline = []
        
        try:
            # 1. Activitats (trucades, reunions, notes de CRM)
            activitats = self.db.query(models.Activitat)\
                .filter(models.Activitat.municipi_id == municipi_id)\
                .order_by(desc(models.Activitat.data_activitat))\
                .limit(limit)\
                .all()
            
            for a in activitats:
                timeline.append({
                    "tipus": a.tipus_activitat.value if hasattr(a.tipus_activitat, 'value') else str(a.tipus_activitat),
                    "data": a.data_activitat,
                    "contingut": a.contingut if isinstance(a.contingut, str) else json.dumps(a.contingut),
                    "notes": a.notes_comercial,
                    "font": "activitat"
                })
                
            # 2. Emails
            emails = self.db.query(models.Email)\
                .filter(models.Email.municipi_id == municipi_id)\
                .order_by(desc(models.Email.data_enviament if hasattr(models.Email, 'data_enviament') else models.Email.data_email))\
                .limit(limit)\
                .all()
                
            for e in emails:
                timeline.append({
                    "tipus": f"email_{e.direccio}",
                    "data": e.data_enviament if hasattr(e, 'data_enviament') else e.data_email,
                    "contingut": e.assumpte,
                    "notes": (e.cos[:350] + "...") if e.cos and len(e.cos) > 350 else e.cos,
                    "font": "email"
                })
                
            # 3. Tasques
            tasques = self.db.query(models.Tasca)\
                .filter(models.Tasca.municipi_id == municipi_id)\
                .filter(models.Tasca.estat == "pendent")\
                .all()
            for t in tasques:
                timeline.append({
                    "tipus": "tasca",
                    "data": t.data_venciment,
                    "contingut": f"Tasca pendent: {t.titol}",
                    "notes": t.descripcio,
                    "font": "task",
                    "prioritat": t.prioritat
                })

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error carregant context de l'agent: {e}")
        
        timeline.sort(key=lambda x: x["data"] if x["data"] else datetime.min.replace(tzinfo=timezone.utc), reverse=True)
        return timeline[:limit]

    async def _call_llm(self, messages: List[Dict[str, str]], skill: str, temperature: float = 0.7, json_mode: bool = False, model: Optional[str] = None):
        from .openrouter_client import call_openrouter
        model_to_use = model or "moonshotai/kimi-k2-thinking"
        return await call_openrouter(messages, model=model_to_use, temperature=temperature, json_mode=json_mode)

    async def analitzar_context(self, municipi_id: UUID) -> Dict[str, Any]:
        activitats = self._load_context(municipi_id)
        
        if not activitats:
            return {
                "ultim_contacte": None,
                "dies_silence": 0,
                "bloquejos": [],
                "sentiment": "neutre"
            }

        ultima_act = activitats[0]
        data_act = ultima_act.get("data")
        dies_silenci = 0
        data_str = None

        if data_act:
            if isinstance(data_act, str):
                from dateutil import parser
                data_act = parser.parse(data_act)
            # Normalize to date for comparison
            d_now = datetime.now(timezone.utc).date()
            d_act = data_act.date() if hasattr(data_act, 'date') else data_act
            dies_silenci = (d_now - d_act).days
            data_str = d_act.strftime("%Y-%m-%d")
        
        bloquejos = []
        if dies_silenci > 15:
            bloquejos.append(f"Sense resposta des de fa {dies_silenci} dies")

        return {
            "ultim_contacte": {
                "tipus": ultima_act.get("tipus"),
                "data": data_str,
                "notes": ultima_act.get("notes")
            },
            "dies_silence": dies_silenci,
            "bloquejos": bloquejos,
            "sentiment": "positiu" if dies_silenci < 5 else "neutre"
        }

    async def recomanar_accio(self, municipi_id: UUID) -> Dict[str, Any]:
        context_data = await self.analitzar_context(municipi_id)
        municipi = self.db.query(models.Municipi).get(municipi_id)
        
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
        municipi = self.db.query(models.Municipi).get(municipi_id)
        contacte = self.db.query(models.Contacte).get(contacte_id) if contacte_id else None
        context_data = await self.analitzar_context(municipi_id)
        
        prompt_key = f"redactar_email.{tipus}"
        try:
            system_prompt = prompt_manager.get_prompt(prompt_key)
        except:
            system_prompt = prompt_manager.get_prompt("redactar_email")

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
        context_str = ""
        if municipi_id:
            municipi = self.db.query(models.Municipi).get(municipi_id)
            if municipi:
                context_data = await self.analitzar_context(municipi.id)
                contactes_info = [
                    f"{c.nom} ({c.carrec}) - Email: {c.email}" 
                    for c in municipi.contactes if c.actiu
                ]

                diagnostics = {
                    "angle": getattr(municipi, 'angle_personalitzacio', "Cap angle definit."),
                    "etapa_desc": str(getattr(municipi, 'etapa_actual', 'n/a')),
                    "valor_setup": str(getattr(municipi, 'valor_setup', 0)),
                    "valor_llicencia": str(getattr(municipi, 'valor_llicencia', 0)),
                    "temperatura": str(getattr(municipi, 'temperatura', 'fred')),
                    "blocker_actual": str(getattr(municipi, 'blocker_actual', 'cap'))
                }

                h_memory = await memory_engine.build_hierarchical_context(self.db, municipi.id, [])
                
                context_str = f"""
CONTEXT MUNICIPI {municipi.nom}:
{json.dumps(context_data, indent=2)}

DIAGNÒSTIC I ESTRATÈGIA:
{json.dumps(diagnostics, indent=2)}

CONTACTES ACTIUS:
{", ".join(contactes_info) if contactes_info else "Cap contacte registrat."}

MEMÒRIA ESTRATÈGICA:
{h_memory}
"""
        else:
            # Global context
            try:
                stats = self.db.query(
                    models.Municipi.etapa_actual, 
                    func.count(models.Municipi.id)
                ).group_by(models.Municipi.etapa_actual).all()
                etapa_stats = {str(etapa): count for etapa, count in stats}

                context_str = f"""
VISIÓ D'ÀGUILA (CONTEXT GLOBAL CRM):
RECOMPTE PER ETAPA:
{json.dumps(etapa_stats, indent=2)}
"""
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error carregant context global: {e}")
                context_str = "CONTEXT GLOBAL: No s'ha pogut carregar la informació."

        system_prompt = prompt_manager.render_prompt("xat_conversacional", {
            "nom_municipi": municipi.nom if (municipi_id and 'municipi' in locals() and municipi) else "Global",
            "etapa": municipi.etapa_actual if (municipi_id and 'municipi' in locals() and municipi) else "N/A"
        })
        
        memory = await memory_engine.get_or_create_memory(self.db, usuari_id, municipi_id=municipi_id)
        history = memory.history or []
        
        messages = [{"role": "system", "content": f"{system_prompt}\n\n{context_str}"}]
        for h in history[-10:]:
            messages.append(h)
        messages.append({"role": "user", "content": message})
        
        response = await self._call_llm(messages, skill="xat", model=model)
        
        new_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": response["content"]}
        ]
        memory.history = new_history
        memory.updated_at = datetime.now(timezone.utc)
        
        try:
            self.db.commit()
        except:
            self.db.rollback()
            
        return {
            "response": response["content"],
            "model": response["model_usat"]
        }

    async def crear_tasca_agent(self, municipi_id: UUID, titol: str, data_venciment: str, descripcio: str = "") -> dict:
        """Permet a l'IA crear una tasca real al calendari."""
        try:
            from models import Tasca
            from dateutil import parser
            
            # Parse date safely
            try:
                dt_venciment = parser.isoparse(data_venciment)
            except:
                dt_venciment = datetime.now(timezone.utc) + timedelta(days=1)

            tasca = Tasca(
                municipi_id=municipi_id,
                titol=titol,
                data_venciment=dt_venciment,
                descripcio=descripcio,
                prioritat=2,
                estat="pendent"
            )
            self.db.add(tasca)
            
            # Registrar l'acció al timeline
            from models import Activitat, TipusActivitat
            activitat = Activitat(
                municipi_id=municipi_id,
                tipus_activitat=TipusActivitat.sistema,
                notes_comercial=f"IA ha programat una tasca: {titol} per al {dt_venciment.strftime('%d/%m/%Y')}",
                data_activitat=datetime.now(timezone.utc)
            )
            self.db.add(activitat)
            
            self.db.commit()
            return {"status": "success", "id": str(tasca.id), "titol": titol}
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error agent creant tasca: {e}")
            raise e
