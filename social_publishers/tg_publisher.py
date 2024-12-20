from aiogram import Bot
from aiogram.types import FSInputFile
import logging
import aiohttp
import os

logging.basicConfig(level=logging.INFO)

class TGPublisher:
    def __init__(self, bot_token, channel_id):
        self.bot = Bot(token=bot_token)
        self.channel_id = channel_id

    async def download_image(self, image_url, save_path="downloaded_image.jpg"):
        try:
            logging.info(f"Starting image download from URL: {image_url}")
            if os.path.exists(save_path):
                os.remove(save_path)

            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch image. Status code: {response.status}")
                    with open(save_path, "wb") as file:
                        file.write(await response.read())

            if os.path.exists(save_path):
                logging.info(f"Image downloaded and saved as {save_path}")
                return save_path
            else:
                logging.error(f"Failed to save image at {save_path}")
                raise FileNotFoundError(f"Failed to save image at {save_path}")
        except Exception as e:
            logging.error(f"Failed to download image: {e}")
            raise

    async def publish_post(self, content: str, image_path: str):
        """Публикует текст и изображение в Telegram."""
        try:
            # Ограничиваем длину текста для подписи
            content = content[:4096]

            # Убедитесь, что изображение существует
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found at path: {image_path}")

            # Загружаем изображение
            photo = FSInputFile(image_path)
            await self.bot.send_photo(chat_id=self.channel_id, photo=photo, caption=content)
            logging.info("Post successfully published to Telegram")
        except Exception as e:
            logging.error(f"Failed to publish post: {e}")
            raise
