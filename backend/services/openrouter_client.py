import os
import httpx
import logging

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

async def call_openrouter(messages, model="anthropic/claude-3.5-sonnet", json_mode=False, temperature=None):
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY is missing in environment variables.")
        raise ValueError("Configuració de IA incompleta (falta API Key)")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://projectexinoxano.cat",
        "X-Title": "CRM PXX"
    }

    payload = {
        "model": model,
        "messages": messages,
    }
    
    if temperature is not None:
        payload["temperature"] = temperature
        
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    # Normalitzar URL per evitar dobles slashes o slashes faltants
    base_url = OPENROUTER_BASE_URL.rstrip("/")
    if not base_url.endswith("/v1"):
        base_url = f"{base_url}/v1"
    url = f"{base_url}/chat/completions"

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            content = data["choices"][0]["message"]["content"]
            tokens_usats = data.get("usage", {}).get("total_tokens", 0)
            
            return {
                "content": content,
                "model_usat": model,
                "tokens_usats": tokens_usats
            }
        except Exception as e:
            logger.error(f"Error calling OpenRouter: {e}")
            raise
