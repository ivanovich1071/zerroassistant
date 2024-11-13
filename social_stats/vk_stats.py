import requests
import datetime
import json

class VKStats:
    def __init__(self, vk_api_key, group_id):
        self.vk_api_key = vk_api_key
        self.group_id = group_id

    def get_stats(self, start_date, end_date):
        url = 'https://api.vk.com/method/stats.get'
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        start_date = start_date.replace(tzinfo=datetime.timezone.utc)
        end_date = end_date.replace(tzinfo=datetime.timezone.utc)

        start_unix_time = start_date.timestamp()
        end_unix_time = end_date.timestamp()

        params = {
            'access_token': self.vk_api_key,
            'v': '5.236',
            'group_id': self.group_id,
            'timestamp_from': start_unix_time,
            'timestamp_to': end_unix_time
        }
        response = requests.get(url, params=params).json()
        if 'error' in response:
            raise Exception(response['error']['error_msg'])
        else:
            return response['response'][0]

    def get_followers(self):
        url = 'https://api.vk.com/method/groups.getMembers'
        params = {
            'access_token': self.vk_api_key,
            'v': '5.236',
            'group_id': self.group_id
        }
        response = requests.get(url, params=params).json()
        if 'error' in response:
            raise Exception(response['error']['error_msg'])
        else:
            return response['response']['count']

    def get_post_stats(self, post_id):
        url = 'https://api.vk.com/method/wall.getById'
        params = {
            'access_token': self.vk_api_key,
            'v': '5.236',
            'posts': f"-{self.group_id}_{post_id}"
        }
        response = requests.get(url, params=params).json()

        # Отладочный вывод для проверки структуры
        print("Ответ от API ВКонтакте на запрос wall.getById:", response)

        if 'error' in response:
            raise Exception(f"Ошибка получения статистики поста: {response['error']['error_msg']}")

        # Проверка, что 'items' присутствует в ответе
        if 'response' in response and 'items' in response['response']:
            post_data = response['response']['items'][0]  # Доступ к первому элементу в 'items'
            stats = {
                'likes': post_data['likes']['count'],
                'views': post_data['views']['count'] if 'views' in post_data else 0,
                'reposts': post_data['reposts']['count'],
                'comments': post_data['comments']['count']
            }
            return stats
        else:
            raise Exception("Не удалось получить данные для указанного поста: неверная структура ответа.")

    def print_stats(self, stats):
        print("Статистика публикации:")
        for key, value in stats.items():
            print(f"{key.capitalize()}: {value}")

    def save_stats_to_json(self, stats, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=4)
