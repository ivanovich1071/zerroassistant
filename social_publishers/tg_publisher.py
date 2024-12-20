from aiogram import Bot
from aiogram.types import InputFile
import logging
import aiohttp
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class TGPublisher:
    def __init__(self, bot_token, channel_id):
        self.bot = Bot(token=bot_token)
        self.channel_id = channel_id

    async def download_image(self, image_url, save_path="output_image.jpg"):
        """Асинхронно загружает изображение из URL и сохраняет локально."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch image. Status code: {response.status}")
                    with open(save_path, "wb") as file:
                        file.write(await response.read())
            return save_path
        except Exception as e:
            logging.error(f"Failed to download image: {e}")
            raise

    async def publish_post(self, content: str, image_url: str):
        """Публикует текст и изображение в Telegram."""
        try:
            # Скачиваем изображение асинхронно
            image_path = await self.download_image(image_url)

            # Проверяем существование файла
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found at path: {image_path}")

            # Создаём InputFile на основе пути к файлу
            photo = InputFile(image_path)

            # Отправляем изображение с подписью
            await self.bot.send_photo(chat_id=self.channel_id, photo=photo, caption=content)
            logging.info("Post successfully published to Telegram")
        except Exception as e:
            logging.error(f"Failed to publish post: {e}")
            raise
