import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test():
    url = "https://openrouter.ai/api/v1/chat/completions"
    api_key = os.getenv("OPENROUTER_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [{"role": "user", "content": "hi"}]
    }
    
    print(f"Testing POST to {url}")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(url, headers=headers, json=payload)
            print(f"Status: {resp.status_code}")
            print(f"Body: {resp.text[:200]}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test())
