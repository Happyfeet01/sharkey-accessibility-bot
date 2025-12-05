import aiohttp
import json
from config import Config

class MisskeyAPI:
    def __init__(self, config: Config):
        self.config = config
        self.session = aiohttp.ClientSession()
        self.base_url = f"{config.MISSKEY_INSTANCE}/api"

    async def _post(self, endpoint: str, data: dict = None):
        if data is None:
            data = {}
        data["i"] = self.config.MISSKEY_TOKEN
        async with self.session.post(
            f"{self.base_url}{endpoint}", json=data
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def get_bot_user_id(self) -> str:
        response = await self._post("/i")
        return response["id"]

    async def get_followers(self) -> list:
        response = await self._post("/users/followers")
        return [user["id"] for user in response]

    async def get_user_notes(self, user_id: str, since_timestamp: int = None) -> list:
        data = {"userId": user_id}
        if since_timestamp:
            data["sinceId"] = since_timestamp
        response = await self._post("/users/notes", data)
        return response

    async def get_note(self, note_id: str) -> dict:
        response = await self._post("/notes/show", {"noteId": note_id})
        return response

    async def post_reply(self, note_id: str, text: str) -> dict:
        data = {"noteId": note_id, "text": text}
        response = await self._post("/notes/create", data)
        return response