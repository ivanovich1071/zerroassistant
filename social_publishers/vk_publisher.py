import requests
from config import vk_api_key, vk_group_id

class VKPublisher:
    def __init__(self):
        self.vk_api_key = vk_api_key
        self.group_id = vk_group_id

    def upload_photo(self, image_url):
        # Шаг 1: Получение URL для загрузки изображения
        upload_url_response = requests.get(
            'https://api.vk.com/method/photos.getWallUploadServer',
            params={
                'access_token': self.vk_api_key,
                'v': '5.236',
                'group_id': self.group_id
            }
        ).json()

        if 'error' in upload_url_response:
            raise Exception(f"Ошибка получения upload_url: {upload_url_response['error']['error_msg']}")

        upload_url = upload_url_response['response']['upload_url']

        # Шаг 2: Загрузка изображения на сервер ВКонтакте
        image_data = requests.get(image_url).content
        upload_response = requests.post(upload_url, files={'photo': ('image.jpg', image_data)}).json()

        # Вывод отладочной информации после загрузки изображения
        print("Ответ от сервера после загрузки изображения:", upload_response)

        if 'error' in upload_response:
            raise Exception(f"Ошибка загрузки изображения: {upload_response['error']['error_msg']}")

        # Проверка наличия необходимых параметров в ответе
        if not all(key in upload_response for key in ['photo', 'server', 'hash']):
            raise Exception("Отсутствуют необходимые данные для сохранения фотографии: photo, server или hash.")

        # Шаг 3: Сохранение загруженного изображения на стене
        save_response = requests.get(
            'https://api.vk.com/method/photos.saveWallPhoto',
            params={
                'access_token': self.vk_api_key,
                'v': '5.236',
                'group_id': self.group_id,
                'photo': upload_response['photo'],
                'server': upload_response['server'],
                'hash': upload_response['hash']
            }
        ).json()

        # Вывод отладочной информации после сохранения изображения
        print("Ответ от сервера после сохранения фотографии:", save_response)

        if 'error' in save_response:
            raise Exception(f"Ошибка сохранения фотографии: {save_response['error']['error_msg']}")

        # Получение id и owner_id загруженного изображения
        photo_id = save_response['response'][0]['id']
        owner_id = save_response['response'][0]['owner_id']
        return f'photo{owner_id}_{photo_id}'

    def publish_post(self, content, image_url=None):
        params = {
            'access_token': self.vk_api_key,
            'from_group': 1,
            'v': '5.236',
            'owner_id': f'-{self.group_id}',
            'message': content
        }
        if image_url:
            attachment = self.upload_photo(image_url)
            params['attachments'] = attachment

        response = requests.post('https://api.vk.com/method/wall.post', params=params).json()

        if 'error' in response:
            raise Exception(response['error']['error_msg'])
        else:
            post_id = response['response']['post_id']
            print(f"Пост успешно опубликован. ID поста: {post_id}")
            return post_id


