import asyncio
import logging
from typing import Set
from misskey_api import MisskeyAPI
from config import Config
from logic import find_images_without_alt, build_auto_description_text
from ollama import Ollama

logger = logging.getLogger(__name__)

class FollowUpTask:
    def __init__(
        self,
        config: Config,
        misskey: MisskeyAPI,
        note_id: str,
        processed_note_ids: Set[str],
        followers: Set[str],
    ):
        self.config = config
        self.misskey = misskey
        self.note_id = note_id
        self.processed_note_ids = processed_note_ids
        self.followers = followers
        self.ollama = Ollama(config)

    async def run(self):
        try:
            await asyncio.sleep(300)  # Wait 5 minutes
            note = await self.misskey.get_note(self.note_id)
            if not self.is_valid_note(note):
                return
            images_without_alt = find_images_without_alt(note)
            if not images_without_alt:
                return
            logger.info(f"Note {self.note_id} still missing alt text, generating descriptions")
            descriptions = []
            for img in images_without_alt:
                image_bytes = await self.ollama.download_image_bytes(img["url"])
                description = await self.ollama.generate_image_description(image_bytes)
                if description:
                    descriptions.append(description)
            if descriptions:
                description_text = build_auto_description_text(descriptions)
                await self.misskey.post_reply(self.note_id, description_text)
        except Exception as e:
            logger.error(f"Failed to follow up on note {self.note_id}: {e}")

    def is_valid_note(self, note: dict) -> bool:
        if note["userId"] not in self.followers:
            return False
        if note["id"] not in self.processed_note_ids:
            return False
        return True