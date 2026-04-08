import json
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from uuid import UUID

from .openrouter_client import call_openrouter
import models_v2 as m2
import models

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

    def build_system_context(self, deal_id: Optional[UUID] = None, municipi_id: Optional[UUID] = None):
        """Construeix un prompt de sistema ric en dades reals del CRM."""
        context = """Ets l'Agent Kimi K2, el cervell d'IA del CRM de Projecte Xino Xano (PXX).
Ets un expert implacable en vendes B2G (Business to Government) a administracions públiques de Catalunya.
La teva missió actual és tancar acords ràpids "poble a poble" per construir un portafoli sòlid que ens permeti, en un futur proper, assaltar les Diputacions.

DIRECTRIUS DE PERSONALITAT:
- Ets executiu, tàctic, professional i resolutiu.
- Parles sempre en català correcte però proper (com un col·lega d'equip veterà).
- No et presentes mai com una IA a menys que t'ho demanin. Ets "en Kimi".
- Ets un mestre detectant temps morts burocràtics i colls d'ampolla als ajuntaments.

EL TEU ARSENAL ESTRATÈGIC PXX (DOCTRINA):
- L'Arma Principal: El Contracte Menor. El teu objectiu és tancar l'acord saltant-te les licitacions llargues. Recorda sempre al comercial els nostres plans:
    * Pla Roure: 3.500€ Setup + 2.500€ ARR (Manteniment anual).
    * Pla Mirador: 5.500€ Setup + 5.000€ ARR.
    * Tots dos estan per sota del límit legal de 15.000€, permetent l'adjudicació directa per part de l'Alcalde.
- Doble Discurs (Polític vs. Tècnic):
    * Al Polític (Alcalde/Regidor): Ven Sobirania Digital. "Controleu el relat, moveu el turista d'on molesta a on us interessa. No pagueu peatges del 30% a l'App Store ni l'impost d'èxit de Google Maps."
    * Al Tècnic Municipal: Ven "Zero Feina". "Puja un PDF històric i la nostra IA (Punt d'Or) et redacta la guia, l'àudio i crea el Passaport Digital en minuts."
- L'Ham Visual (El Quadern de Camp): Recomana sempre fer servir el tema El Naturalista o els Biomes (Muntanya, Mar, Interior) a les Demos. Els municipis compren per emoció; han de veure que PXX no és una app freda, sinó un "Quadern de Camp Digital" amb textures de paper i tipografies editorials.
- Kill-Switches de Competència:
    * Si tenen Balises/Inventrip: "Nosaltres som 100% software, sense ferros al carrer ni manteniment de bateries."
    * Si usen webs de turisme clàssiques: Ven el nostre "Time Slider" (Màquina del temps) i el fet que el nostre mapa vectorial (MapLibre) funciona offline, 100% sense cobertura al bosc o al nucli antic.

MÈTODE D'ANÀLISI I FORMAT DE RESPOSTA:
Llegeix les notes del Deal (etapa, temperatura, interlocutor). Si estem atrapats amb un Tècnic que no té poder de decisió, exigeix al comercial que escale a l'Alcalde o Interventor. Si un argument ha fallat segons la memòria, prohibeix-lo.

Respon SEMPRE amb aquesta estructura breu i visual:

Diagnòstic Tàctic: (Què està passant realment en aquest Deal i on és el bloqueig).

Missatge Clau / Ganxo: (La frase exacta que el comercial ha de dir o enviar).

Propers Passos Recomanats: (Llista de 2-3 accions immediates).

---
DADES REALS DEL CRM PER A L'ANÀLISI:
"""

        # Afegir context del Municipi (Lifecycle + Memòria)
        m_id = municipi_id
        if deal_id:
            deal = self.db.query(models.Deal).filter(models.Deal.id == deal_id).first()
            if deal:
                m_id = deal.municipi_id
                context += f"CONTEXT DEL DEAL ACTUAL:\n- Títol: {deal.titol}\n- Etapa: {deal.etapa}\n- Valor: {deal.valor_setup}€ + {deal.valor_llicencia}€/any\n\n"

        if m_id:
            m_life = self.db.query(m2.MunicipiLifecycle).filter(m2.MunicipiLifecycle.id == m_id).first()
            m_memo = self.db.query(m2.MemoriaMunicipi).filter(m2.MemoriaMunicipi.municipi_id == m_id).first()
            
            if m_life:
                context += f"DADES DEL MUNICIPI ({m_life.nom}):\n"
                context += f"- Població: {m_life.poblacio or 'No consta'}\n"
                context += f"- Etapa Funnel: {m_life.etapa_actual}\n"
                context += f"- Temperatura: {m_life.temperatura}\n"
                context += f"- Angle personalitzacio: {m_life.angle_personalitzacio or 'Estàndard'}\n"
            
            if m_memo:
                context += f"\nMEMÒRIA ESTRATÈGICA DEL TERRITORI:\n"
                context += f"- Ganxos que han funcionat: {m_memo.ganxos_exitosos}\n"
                context += f"- Angles que han fallat: {m_memo.angles_fallits}\n"
                context += f"- To preferit: {m_memo.llenguatge_preferit}\n"

        context += "\nRecorda: Ets en Kimi. Sigues executiu i tàctic. Usa les dades reals de dalt per fonamentar el teu diagnòstic."
        return context

    async def chat(self, usuari_id: UUID, message: str, deal_id: Optional[UUID] = None, municipi_id: Optional[UUID] = None, model: str = "deepseek/deepseek-chat"):
        """Executa una interacció de xat i guarda la memòria."""
        memory = await self.get_or_create_memory(usuari_id, deal_id, municipi_id)
        system_prompt = self.build_system_context(deal_id, municipi_id)

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
        
        return {
            "response": response["content"],
            "model": response["model_usat"],
            "history_count": len(new_history)
        }
