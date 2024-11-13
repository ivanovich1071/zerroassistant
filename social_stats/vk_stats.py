import requests
import datetime
import json
import time
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VKStats:
    def __init__(self, vk_api_key, group_id):
        self.vk_api_key = vk_api_key
        self.group_id = group_id
        self.base_url = 'https://api.vk.com/method/'
        self.version = '5.236'

    def send_request(self, method, params, max_retries=3):
        """Общий метод для отправки запросов к VK API с поддержкой повторных попыток."""
        url = self.base_url + method
        params.update({'access_token': self.vk_api_key, 'v': self.version})
        for attempt in range(max_retries):
            try:
                response = requests.get(url, params=params).json()
                if 'error' in response:
                    raise Exception(response['error']['error_msg'])
                return response
            except Exception as e:
                logging.error(f"Ошибка запроса к VK API: {e}. Попытка {attempt + 1} из {max_retries}.")
                time.sleep(2)  # Ожидание перед повторной попыткой
        raise Exception("Не удалось выполнить запрос после нескольких попыток")

    def get_stats(self, start_date, end_date):
        """Получение статистики группы за указанный период."""
        start_unix_time = datetime.datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp()
        end_unix_time = datetime.datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp()
        params = {'group_id': self.group_id, 'timestamp_from': start_unix_time, 'timestamp_to': end_unix_time}
        response = self.send_request('stats.get', params)
        return response.get('response', [])[0] if response else {}

    def get_followers(self):
        """Получение количества подписчиков группы."""
        params = {'group_id': self.group_id}
        response = self.send_request('groups.getMembers', params)
        return response.get('response', {}).get('count', 0)

    def get_post_stats(self, post_id):
        """Получение статистики для определенного поста."""
        params = {'posts': f"-{self.group_id}_{post_id}"}
        response = self.send_request('wall.getById', params)

        if 'response' in response and response['response']:
            post_data = response['response'][0]
            stats = {
                'likes': post_data.get('likes', {}).get('count', 0),
                'views': post_data.get('views', {}).get('count', 0),
                'reposts': post_data.get('reposts', {}).get('count', 0),
                'comments': post_data.get('comments', {}).get('count', 0)
            }
            return stats
        else:
            raise Exception("Не удалось получить данные для указанного поста")

    def print_stats(self, stats):
        """Вывод статистики в консоль."""
        logging.info("Статистика публикации:")
        for key, value in stats.items():
            print(f"{key.capitalize()}: {value}")

    def save_stats_to_json(self, stats, filename):
        """Сохранение статистики в файл JSON."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=4)
