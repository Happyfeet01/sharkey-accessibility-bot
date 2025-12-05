import aiohttp
import base64
from config import Config

class Ollama:
    def __init__(self, config: Config):
        self.config = config
        self.session = aiohttp.ClientSession()

    async def download_image_bytes(self, url: str) -> bytes:
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.read()

    async def generate_image_description(self, image_bytes: bytes) -> str:
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        data = {
            "model": self.config.OLLAMA_MODEL,
            "prompt": "Beschreibe dieses Bild in 1–2 kurzen, sachlichen Sätzen auf Deutsch ohne Emojis oder Spekulationen.",
            "images": [image_base64],
        }
        async with self.session.post(
            self.config.OLLAMA_URL, json=data
        ) as response:
            response.raise_for_status()
            result = await response.json()
            return result.get("response", "")