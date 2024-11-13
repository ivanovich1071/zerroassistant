from vk_publisher import VKPublisher
from vk_stats import VKStats
from config import vk_api_key, vk_group_id

# Инициализация
publisher = VKPublisher()
stats = VKStats(vk_api_key, vk_group_id)

# Публикация поста
post_id = publisher.publish_post(
    "поставка перемешивающих устройств промышленного назначения с диаметром импеллера 1500мм",
    image_url="https://oaidalleapiprodscus.blob.core.windows.net/private/org-Nu6i18ndQcChxhFFK70fdZQ9/user-1g41377aACrx3eVYJTxGOmKO/img-mW6LttiLTcFZTiqqhrf4BVgT.png?st=2024-11-13T07%3A17%3A27Z&se=2024-11-13T09%3A17%3A27Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-11-12T19%3A55%3A08Z&ske=2024-11-13T19%3A55%3A08Z&sks=b&skv=2024-08-04&sig=oXrFo9xT8U7J1mGj4DPbOjfl4Fb2YNbrIClhL0ZuFMw%3D"
)

# Получение статистики по опубликованному посту
if post_id:
    # Получаем статистику поста
    post_stats = stats.get_post_stats(post_id)

    # Выводим и сохраняем статистику
    stats.print_stats(post_stats)
    stats.save_stats_to_json(post_stats, 'post_stats.json')
