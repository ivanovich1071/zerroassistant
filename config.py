from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значений переменных
openai_key = os.getenv('openai_key')
vk_api_key = os.getenv('vk_api_key')
vk_group_id = os.getenv('vk_group_id')

# Новые переменные для Telegram
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_channel_id = os.getenv('TELEGRAM_CHANNEL_ID')

# Проверка значений (опционально для отладки)
#if __name__ == "__main__":
   # print(f"OpenAI Key: {openai_key}")
    #print(f"VK API Key: {vk_api_key}")
    #print(f"VK Group ID: {vk_group_id}")
    #print(f"Telegram Bot Token: {telegram_bot_token}")
    #print(f"Telegram Channel ID: {telegram_channel_id}")