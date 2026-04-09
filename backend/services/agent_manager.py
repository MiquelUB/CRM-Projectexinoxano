import os
import yaml
import logging
from typing import Dict, Any, Optional
from .openrouter_client import call_openrouter

logger = logging.getLogger(__name__)

from .prompt_manager import prompt_manager

class KimiAgentManager:
    """Proxy per mantenir compatibilitat mentre es migra al PromptManager centralitzat."""
    def get_skill_system_prompt(self, skill_name: str, perfil: Optional[str] = None, situacio: Optional[str] = None) -> str:
        # Intentem mapejar a la nova estructura
        return prompt_manager.render_prompt(skill_name, {"perfil": perfil, "situacio": situacio})

    async def call_skill(self, skill_name: str, user_content: str, sub_key: Optional[str] = None, json_mode: bool = False, model: str = "google/gemini-2.0-flash-001") -> Dict[str, Any]:
        system_prompt = self.get_skill_system_prompt(skill_name, sub_key)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        return await call_openrouter(messages, model=model, json_mode=json_mode)

kimi_agent = KimiAgentManager()
