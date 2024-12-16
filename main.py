from app import create_app
import logging
from logging.handlers import RotatingFileHandler
import os

# Создаем приложение Flask
app = create_app()

# Настройка логирования
if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Application startup')

# Точка входа в приложение
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        app.logger.error(f"Application error: {e}")
