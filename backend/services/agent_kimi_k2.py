import json
import os
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta

from .prompt_manager import prompt_manager
from .memory_engine import memory_engine
import models_v2
import models
import logging

logger = logging.getLogger(__name__)

class AgentKimiK2:
    def __init__(self, db: Session):
        self.db = db

    def _load_context(self, municipi_id: UUID, limit: int = 50) -> List[Dict[str, Any]]:
        """Retorna el timeline complet d'activitats del municipi (V2 + Emails V2 + Emails V1)."""
        # 1. Activitats V2 (trucades, reunions, notes de CRM)
        activitats = self.db.query(models_v2.ActivitatsMunicipi)\
            .filter(models_v2.ActivitatsMunicipi.municipi_id == municipi_id)\
            .order_by(desc(models_v2.ActivitatsMunicipi.data_activitat))\
            .limit(limit)\
            .all()
        
        timeline = []
        for a in activitats:
            timeline.append({
                "tipus": a.tipus_activitat.value if hasattr(a.tipus_activitat, 'value') else str(a.tipus_activitat),
                "data": a.data_activitat,
                "contingut": a.contingut if isinstance(a.contingut, str) else json.dumps(a.contingut),
                "notes": a.notes_comercial,
                "font": "v2_activitat"
            })
            
        # 2. Emails V2 (el nou sistema d'emails)
        emails_v2 = self.db.query(models_v2.EmailV2)\
            .filter(models_v2.EmailV2.municipi_id == municipi_id)\
            .order_by(desc(models_v2.EmailV2.data_enviament))\
            .limit(limit)\
            .all()
            
        for e in emails_v2:
            timeline.append({
                "tipus": f"email_{e.direccio}",
                "data": e.data_enviament,
                "contingut": e.assumpte,
                "notes": (e.cos[:350] + "...") if e.cos and len(e.cos) > 350 else e.cos,
                "font": "v2_email",
                "sentiment": e.sentiment_resposta if e.direccio == 'entrada' else 'N/A',
                "obert": e.obert if e.direccio == 'sortida' else 'N/A'
            })
            
        # 3. Emails V1 (legacy, via Deals)
        emails_v1 = self.db.query(models.Email)\
            .join(models.Deal, models.Email.deal_id == models.Deal.id)\
            .filter(models.Deal.municipi_id == municipi_id)\
            .order_by(desc(models.Email.data_email))\
            .limit(limit)\
            .all()
        
        for e in emails_v1:
            timeline.append({
                "tipus": f"email_{e.direccio}",
                "data": e.data_email,
                "contingut": e.assumpte,
                "notes": (e.cos[:200] + "...") if e.cos and len(e.cos) > 200 else e.cos,
                "font": "v1_email",
                "de": e.from_address
            })
        
        # 4. Re-ordenar per data descendents
        timeline.sort(key=lambda x: x["data"] if x["data"] else datetime.min, reverse=True)
        return timeline[:limit]

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
        data_act = ultima_act.get("data")
        if data_act:
            if isinstance(data_act, str):
                from dateutil import parser
                data_act = parser.parse(data_act)
            dies_silenci = (datetime.now().date() - data_act.date()).days
            data_str = data_act.strftime("%Y-%m-%d")
        else:
            dies_silenci = 0
            data_str = None
        
        bloquejos = []
        # Regla: Silenci prolongat
        if dies_silenci > 15:
            bloquejos.append(f"Sense resposta des de fa {dies_silenci} dies")

        # Regla: Demo sense seguiment (reunio)
        foie_demo = any(a.get("tipus") in ["reunio", "trucada"] for a in activitats[:5])
        if foie_demo and dies_silenci > 7:
            bloquejos.append("Oportunitat freda: Últim contacte rellevant fa més de 7 dies")

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
        if municipi_id:
            # B-01: Fallback logic V1 -> V2
            municipi = self.db.query(models_v2.MunicipiLifecycle).get(municipi_id)
            
            # B-01: Fallback logic V1 -> V2 amb protecció contra columnes inexistents
            if not municipi:
                logger.info(f"Municipi {municipi_id} no trobat a V2 per ID directe, buscant fallback V1...")
                
                # Intentem buscar primer pel camp de migració directament (v1_id)
                try:
                    municipi = self.db.query(models_v2.MunicipiLifecycle).filter(
                        models_v2.MunicipiLifecycle.municipi_v1_id == municipi_id
                    ).first()
                except Exception as e:
                    logger.warning(f"Error consultant municipi_v1_id (possiblement la columna no existeix): {e}")
                    municipi = None
                
                if not municipi:
                    # Segon nivell de fallback: per nom via models V1
                    try:
                        municipi_v1 = self.db.query(models.Municipi).filter(models.Municipi.id == municipi_id).first()
                        if municipi_v1:
                            municipi = self.db.query(models_v2.MunicipiLifecycle).filter(
                                models_v2.MunicipiLifecycle.nom == municipi_v1.nom
                            ).first()
                            if municipi:
                                logger.info(f"Sincronitzat municipi V1 '{municipi_v1.nom}' via Match per Nom.")
                    except Exception as e:
                        logger.error(f"Error en fallback per nom V1: {e}")
            
            if municipi:
                # Carregar context base d'activitats
                context_data = await self.analitzar_context(municipi.id)
                
                # B-03 & B-06: Expandir context amb dades de diagnòstic i contactes (amb protecció de nul·les)
                contactes_info = []
                try:
                    if hasattr(municipi, 'contactes') and municipi.contactes:
                        contactes_info = [
                            f"{c.nom} ({c.carrec}) - Email: {c.email}" 
                            for c in municipi.contactes if c.actiu
                        ]
                except Exception as e:
                    logger.warning(f"Error carregant contactes per al context: {e}")

                diagnostics = {}
                try:
                    diagnostics = {
                        "digital": getattr(municipi, 'diagnostic_digital', {}),
                        "angle": getattr(municipi, 'angle_personalitzacio', "Cap angle definit."),
                        "etapa_desc": str(getattr(municipi, 'etapa_actual', 'n/a'))
                    }
                except Exception as e:
                    logger.warning(f"Error carregant diagnòstics per al context: {e}")
                
                # Integrar Memòria Jeràrquica
                h_memory = await memory_engine.build_hierarchical_context(self.db, municipi.id, [])
                
                context_str = f"""
CONTEXT MUNICIPI {municipi.nom}:
{json.dumps(context_data, indent=2)}

DIAGNÒSTIC I ESTRATÈGIA:
{json.dumps(diagnostics, indent=2)}

CONTACTES ACTIUS:
{", ".join(contactes_info) if contactes_info else "Cap contacte registrat."}

MEMÒRIA ESTRATÈGICA (KIMI MEMORY V2):
{h_memory}
"""
            else:
                logger.warning(f"Municipi {municipi_id} no trobat per al xat (ni a V2 ni fallback V1).")
                context_str = "CONTEXT: El municipi seleccionat no existeix a la base de dades. Demana a l'usuari que verifiqui si el municipi està correctament importat."
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
