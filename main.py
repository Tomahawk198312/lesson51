import src.config
import flet as ft
from src.main import ChatApp

async def main(page: ft.Page):
    app = ChatApp()
    await app.main(page)

ft.app(target=main)