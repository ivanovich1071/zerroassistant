from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from app.models import User
from app import db
from generators.text_gen import PostGenerator
from generators.image_gen import ImageGenerator
from social_publishers.vk_publisher import VKPublisher
from social_stats.vk_stats import VKStats
from config import openai_key
from social_publishers.tg_publisher import TGPublisher
from config import telegram_bot_token, telegram_channel_id
import asyncio

smm_bp = Blueprint('smm', __name__)


@smm_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')


# Маршрут для страницы настроек, где пользователь может ввести vk_api_id и vk_group_id
@smm_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # Перенаправление на страницу входа, если пользователь не авторизован

    user = User.query.get(session['user_id'])  # Получаем текущего пользователя из базы данных

    if request.method == 'POST':
        # Сохраняем введенные пользователем vk_api_id и vk_group_id
        user.vk_api_id = request.form['vk_api_id']
        user.vk_group_id = request.form['vk_group_id']
        db.session.commit()  # Сохраняем изменения в базе данных
        flash('Настройки сохранены!', 'success')  # Уведомляем пользователя о сохранении настроек

    return render_template('settings.html', user=user)  # Отображаем страницу настроек



@smm_bp.route('/post-generator', methods=['GET', 'POST'])
def post_generator():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        tone = request.form['tone']
        topic = request.form['topic']
        generate_image = 'generate_image' in request.form
        auto_post = 'auto_post' in request.form
        tg_post = 'tg_post' in request.form  # Новый флаг для публикации в Telegram

        user = User.query.get(session['user_id'])

        post_gen = PostGenerator(openai_key, tone, topic)
        post_content = post_gen.generate_post()

        image_url = None
        if generate_image:
            image_gen = ImageGenerator(openai_key)
            image_prompt = post_gen.generate_post_image_description()
            image_url = image_gen.generate_image(image_prompt)

        # Публикация в Telegram
        if tg_post:
            tg_publisher = TGPublisher(telegram_bot_token, telegram_channel_id)
            asyncio.run(tg_publisher.publish_post(post_content, image_url))
            flash('Post published to Telegram successfully!', 'success')

        return render_template('post_generator.html', post_content=post_content, image_url=image_url)

    return render_template('post_generator.html')
# Маршрут для страницы статистики ВКонтакте
@smm_bp.route('/vk-stats', methods=['GET'])
def vk_stats():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # Перенаправление на вход, если пользователь не авторизован

    user = User.query.get(session['user_id'])  # Получаем текущего пользователя из базы данных

    # Проверка на наличие vk_api_id и vk_group_id у пользователя
    if not user.vk_api_id or not user.vk_group_id:
        flash("VK API ID и Group ID необходимы для получения статистики.", "warning")
        return redirect(url_for('smm.settings'))  # Перенаправляем пользователя на страницу настроек

    # Создаем экземпляр класса VKStats для получения статистики
    vk_stats = VKStats(user.vk_api_id, user.vk_group_id)
    try:
        followers_count = vk_stats.get_followers()  # Запрос на получение количества подписчиков в ВКонтакте
    except Exception as e:
        flash(f"Ошибка при получении статистики VK: {e}", "danger")
        followers_count = "Ошибка"  # Отображение ошибки в случае неудачи

    # Формируем словарь со статистикой для отображения на странице
    stats = {
        "Подписчики": followers_count,
        "Лайки": "N/A",
        "Комментарии": "N/A",
        "Репосты": "N/A"
    }

    return render_template('vk_stats.html', stats=stats)  # Отображаем страницу vk_stats.html с данными
