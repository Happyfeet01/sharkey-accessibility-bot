import asyncio
import logging
from typing import Set
from config import Config
from misskey_api import MisskeyAPI
from logic import (
    find_images_without_alt,
    is_valid_note,
    build_reminder_text,
    build_auto_description_text,
)
from followup import FollowUpTask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AccessibilityBot:
    def __init__(self, config: Config):
        self.config = config
        self.misskey = MisskeyAPI(config)
        self.followers: Set[str] = set()
        self.processed_note_ids: Set[str] = set()
        self.followup_tasks: Set[asyncio.Task] = set()
        self.running = False

    async def fetch_followers(self):
        try:
            followers = await self.misskey.get_followers()
            self.followers = set(followers)
            logger.info(f"Updated followers: {len(self.followers)} followers")
        except Exception as e:
            logger.error(f"Failed to fetch followers: {e}")

    async def process_notes(self):
        try:
            bot_user_id = await self.misskey.get_bot_user_id()
            for follower_id in self.followers:
                notes = await self.misskey.get_user_notes(follower_id)
                for note in notes:
                    if note["id"] in self.processed_note_ids:
                        continue
                    if not is_valid_note(note, bot_user_id):
                        continue
                    self.processed_note_ids.add(note["id"])
                    images_without_alt = find_images_without_alt(note)
                    if images_without_alt:
                        logger.info(f"Found note {note['id']} with missing alt text")
                        await self.handle_note_with_missing_alt(note, images_without_alt)
        except Exception as e:
            logger.error(f"Failed to process notes: {e}")

    async def handle_note_with_missing_alt(self, note: dict, images_without_alt: list):
        try:
            if not await self.is_follower(note["userId"]):
                return
            reminder_text = build_reminder_text()
            await self.misskey.post_reply(note["id"], reminder_text)
            followup_task = asyncio.create_task(
                FollowUpTask(
                    self.config,
                    self.misskey,
                    note["id"],
                    self.processed_note_ids,
                    self.followers,
                ).run()
            )
            self.followup_tasks.add(followup_task)
            followup_task.add_done_callback(self.followup_tasks.discard)
        except Exception as e:
            logger.error(f"Failed to handle note {note['id']}: {e}")

    async def is_follower(self, user_id: str) -> bool:
        return user_id in self.followers

    async def run(self):
        self.running = True
        logger.info("Starting accessibility bot...")
        while self.running:
            try:
                await self.fetch_followers()
                await self.process_notes()
                await asyncio.sleep(self.config.CHECK_INTERVAL_SECONDS)
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(self.config.CHECK_INTERVAL_SECONDS)

    async def stop(self):
        self.running = False
        for task in self.followup_tasks:
            task.cancel()
        logger.info("Stopping accessibility bot...")

async def main():
    config = Config()
    bot = AccessibilityBot(config)
    try:
        await bot.run()
    except KeyboardInterrupt:
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())