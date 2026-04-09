import os
import yaml
import logging
from typing import Dict, Any, Optional
from .openrouter_client import call_openrouter

logger = logging.getLogger(__name__)

class KimiAgentManager:
    _instance = None
    _prompts = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KimiAgentManager, cls).__new__(cls)
            cls._instance._load_prompts()
        return cls._instance

    def _load_prompts(self):
        """Carrega el fitxer prompts.yaml des de l'arrel del backend."""
        try:
            # Intentar diverses rutes depenent d'on s'executi
            possible_paths = [
                "prompts.yaml",
                "backend/prompts.yaml",
                "../prompts.yaml"
            ]
            path_found = False
            for p in possible_paths:
                if os.path.exists(p):
                    with open(p, 'r', encoding='utf-8') as f:
                        self._prompts = yaml.safe_load(f)
                        path_found = True
                        logger.info(f"Prompts carregats correctament des de {p}")
                        break
            
            if not path_found:
                 logger.error("No s'ha trobat el fitxer prompts.yaml")
                 self._prompts = {"kimi_v2": {"personalitat": "Ets en Kimi.", "skills": {}}}
                 
        except Exception as e:
            logger.error(f"Error carregant prompts.yaml: {e}")
            self._prompts = {}

    def get_base_context(self) -> str:
        """Retorna la personalitat i doctrina base."""
        kimi = self._prompts.get('kimi_v2', {})
        return f"{kimi.get('personalitat', '')}\n\nDOCTRINA PXX:\n{kimi.get('doctrina_pxx', '')}"

    def get_skill_system_prompt(self, skill_name: str, perfil: Optional[str] = None, situacio: Optional[str] = None) -> str:
        """Construeix el prompt de sistema combinant personalitat, habilitat, perfil i situació."""
        kimi = self._prompts.get('kimi_v2', {})
        skills = kimi.get('skills', {})
        skill_data = skills.get(skill_name, {})
        
        # Base: Personalitat + Doctrina
        system_parts = [self.get_base_context()]
        
        # Skill Base
        if isinstance(skill_data, dict):
            if 'base_system' in skill_data:
                system_parts.append(skill_data['base_system'])
            if 'system' in skill_data:
                system_parts.append(skill_data['system'])
            
            # Perfil (Target)
            if perfil and 'perfils' in skill_data:
                perfil_prompt = skill_data['perfils'].get(perfil)
                if perfil_prompt:
                    system_parts.append(f"TARGET (PERFIL): {perfil_prompt}")
            
            # Situació
            if situacio and 'situacions' in skill_data:
                situ_prompt = skill_data['situacions'].get(situacio)
                if situ_prompt:
                    system_parts.append(f"SITUACIÓ ACTUAL: {situ_prompt}")
        elif isinstance(skill_data, str):
            system_parts.append(skill_data)

        return "\n\n---\n\n".join(system_parts)

    async def call_skill(self, skill_name: str, user_content: str, sub_key: Optional[str] = None, json_mode: bool = False, model: str = "moonshotai/kimi-k2") -> Dict[str, Any]:
        """Executa una crida a l'IA usant una habilitat específica."""
        system_prompt = self.get_skill_system_prompt(skill_name, sub_key)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        try:
            return await call_openrouter(messages, model=model, json_mode=json_mode)
        except Exception as e:
            logger.error(f"Error en crida a skill {skill_name}: {e}")
            raise

# Instància única per a tot el sistema
kimi_agent = KimiAgentManager()
