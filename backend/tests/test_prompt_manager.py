import os
import sys
import unittest
import time
from unittest.mock import patch, MagicMock

# Afegim el path del backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.prompt_manager import PromptManager

class TestPromptManager(unittest.TestCase):
    def setUp(self):
        self.manager = PromptManager()

    def test_load_prompts(self):
        """Verificar que carregar prompts no llança errors i conté les seccions base."""
        self.manager.load_prompts()
        self.assertIn("kimi_k2", self.manager._prompts)
        self.assertIn("skills", self.manager._prompts["kimi_k2"])

    def test_get_prompt_skill(self):
        """Verificar obtenint prompt d'una skill."""
        prompt = self.manager.get_prompt("xat_conversacional")
        self.assertIsInstance(prompt, str)
        self.assertIn("Ets el Kimi K2", prompt)

    def test_render_prompt_with_vars(self):
        """Verificar renderització amb variables Jinja2."""
        context = {"nom_municipi": "Guardamar", "etapa": "Demo"}
        rendered = self.manager.render_prompt("analitzar_context", context)
        
        # Ha de contenir la personalitat (base) i la variable renderitzada
        self.assertIn("Agent Kimi K2", rendered)
        self.assertIn("Guardamar", rendered)
        self.assertIn("Demo", rendered)

    def test_cache_and_file_change(self):
        """Verificar que detecta canvis al fitxer (simulat)."""
        initial_mtime = self.manager._last_modified
        
        # Simulem que el fitxer no ha canviat
        with patch('os.path.getmtime') as mock_mtime:
            mock_mtime.return_value = initial_mtime
            self.manager._ensure_loaded()
            # No hauria de cridar load_prompts de nou si usem un mock de seguiment podríem veure-ho
            
        # Simulem canvi de fitxer
        with patch('os.path.getmtime') as mock_mtime:
            mock_mtime.return_value = initial_mtime + 100
            with patch.object(PromptManager, 'load_prompts') as mock_load:
                self.manager._ensure_loaded()
                mock_load.assert_called_once()

if __name__ == '__main__':
    unittest.main()
