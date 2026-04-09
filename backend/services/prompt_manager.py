import os
import yaml
from jinja2 import Template
import logging

logger = logging.getLogger(__name__)

class PromptManager:
    _instance = None
    _prompts = {}
    _last_modified = 0
    _file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "prompts.yaml")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PromptManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._ensure_loaded()

    def _ensure_loaded(self):
        """Carrega els prompts si no estan carregats o si el fitxer ha canviat."""
        try:
            if not os.path.exists(self._file_path):
                logger.error(f"Fitxer de prompts no trobat: {self._file_path}")
                return

            mtime = os.path.getmtime(self._file_path)
            if mtime > self._last_modified or not self._prompts:
                self.load_prompts()
                self._last_modified = mtime
                logger.info("Prompts recarregats correctament (cache hit/refresh).")
        except Exception as e:
            logger.error(f"Error en _ensure_loaded: {e}")

    def load_prompts(self):
        """Llegeix el fitxer YAML."""
        with open(self._file_path, 'r', encoding='utf-8') as f:
            self._prompts = yaml.safe_load(f)

    def get_prompt(self, skill, variant=None):
        """Retorna el system prompt per a una skill i variant opcional."""
        self._ensure_loaded()
        
        try:
            # Busquem a kimi_k2.skills
            skills = self._prompts.get("kimi_k2", {}).get("skills", {})
            skill_data = skills.get(skill)
            
            if isinstance(skill_data, dict):
                if variant:
                    return skill_data.get(variant, "")
                return skill_data.get("system", "")
            elif isinstance(skill_data, str):
                return skill_data
                
            return ""
        except Exception as e:
            logger.error(f"Error obtenint prompt per {skill}.{variant}: {e}")
            return ""

    def render_prompt(self, skill, context_vars, variant=None):
        """Renderitza un prompt amb variables Jinja2."""
        raw_prompt = self.get_prompt(skill, variant)
        if not raw_prompt:
            return ""
        
        try:
            template = Template(raw_prompt)
            # Afegim la personalitat base si no està ja inclosa
            personality = self._prompts.get("kimi_k2", {}).get("personalitat", "")
            rendered = template.render(**context_vars)
            
            # El prompt final és Personalitat + Skill renderitzada
            return f"{personality}\n\n{rendered}"
        except Exception as e:
            logger.error(f"Error renderitzant prompt per {skill}: {e}")
            return raw_prompt

# Instància global per a facilitat d'ús
prompt_manager = PromptManager()
