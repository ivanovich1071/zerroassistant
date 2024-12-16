from aiogram import Bot
from aiogram.types import Message
import logging

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

class TGPublisher:
    def __init__(self, bot_token, channel_id):
        self.bot = Bot(token=bot_token)
        self.channel_id = channel_id

    async def publish_post(self, content: str, image_url: str = None):
        try:
            if image_url:
                await self.bot.send_photo(chat_id=self.channel_id, photo=image_url, caption=content)
            else:
                await self.bot.send_message(chat_id=self.channel_id, text=content)
            logging.info("Post successfully published to Telegram")
        except Exception as e:
            logging.error(f"Failed to publish post: {e}")
            raise
