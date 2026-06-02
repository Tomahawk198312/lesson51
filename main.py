import flet as ft
from dotenv import load_dotenv
import os

# Загружаем .env из папки assets (для локального запуска)
load_dotenv(os.path.join(os.path.dirname(__file__), 'assets', '.env'))

# При сборке APK переменные окружения уже установлены через src.config
try:
    import src.config
except ImportError:
    pass

from src.main import ChatApp

def main(page: ft.Page):
    app = ChatApp()
    app.main(page)

if __name__ == "__main__":
    ft.run(main)