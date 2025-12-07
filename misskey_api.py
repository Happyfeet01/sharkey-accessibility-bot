import aiohttp
import logging
from config import Config  # Changed from 'config' to 'Config'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MisskeyAPI:
    def __init__(self):
        self.base_url = Config.MISSKEY_INSTANCE  # Changed from 'config' to 'Config'
        self.token = Config.MISSKEY_TOKEN  # Changed from 'config' to 'Config'
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def _post(self, endpoint, data):
        url = f"{self.base_url}{endpoint}"
        data["i"] = self.token
        try:
            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_msg = await response.text()
                    logger.error(f"Failed to fetch data: {response.status}, message='{error_msg}', url='{url}'")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def get_bot_user_id(self):
        data = {}
        response = await self._post("/api/i", data)
        return response.get("id")

    async def get_followers(self):
        bot_user_id = await self.get_bot_user_id()
        data = {"userId": bot_user_id, "limit": 100}  # Added userId and limit
        response = await self._post("/api/users/followers", data)
        if response is None:
            return []
        return [user["id"] for user in response]

    async def get_user_notes(self, user_id, since_timestamp=None):
        data = {"userId": user_id}
        if since_timestamp:
            data["sinceId"] = since_timestamp
        response = await self._post("/api/users/notes", data)
        return response

    async def get_note(self, note_id):
        data = {"noteId": note_id}
        response = await self._post("/api/notes/show", data)
        return response

    async def post_reply(self, note_id, text):
        data = {"replyId": note_id, "text": text}
        response = await self._post("/api/notes/create", data)
        return response