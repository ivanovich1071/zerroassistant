from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значений переменных
openai_key = os.getenv('openai_key')
vk_api_key = os.getenv('vk_api_key')
vk_group_id = os.getenv('vk_group_id')