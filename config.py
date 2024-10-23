# config.py
from dotenv import load_dotenv
import os

load_dotenv()  # Загрузка переменных окружения из файла .env

BOT_TOKEN = os.getenv('BOT_TOKEN')