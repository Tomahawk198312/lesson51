import flet as ft
from .api.openrouter import OpenRouterClient
from .ui.styles import AppStyles
from .ui.components import MessageBubble, ModelSelector
from .utils.cache import ChatCache
from .utils.logger import AppLogger
from .utils.analytics import Analytics
from .utils.monitor import PerformanceMonitor
import asyncio
import time
import json
from datetime import datetime
import os


def show_error_snack(page, message):
    snack = ft.SnackBar(
        content=ft.Text(message, color=ft.Colors.RED_500, weight=ft.FontWeight.BOLD),
        bgcolor=ft.Colors.GREY_900,
        duration=5000,
    )
    page.overlay.append(snack)
    snack.open = True
    page.update()


class ChatApp:
    def __init__(self):
        self.logger = AppLogger()
        self.monitor = PerformanceMonitor()
        self.balance_text = ft.Text("Баланс: Загрузка...", **AppStyles.BALANCE_TEXT)
        self.cache = None
        self.analytics = None
        self.api_client = None
        self.exports_dir = None

    def main(self, page: ft.Page):

        # Диагностика
        page.add(ft.Text("Приложение запущено", color=ft.Colors.WHITE))
        page.update()

        # 1. Загрузка конфигурации
        try:
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("API ключ не найден в .env")
            page.controls.append(ft.Text(f"Ключ загружен: {api_key[:8]}...", color=ft.Colors.GREEN))
        except Exception as e:
            page.controls.append(ft.Text(f"Ошибка загрузки конфигурации: {e}", color=ft.Colors.RED))
            page.update()
            return

        # 2. Создание директорий и кэша
        try:
            app_dir = os.path.dirname(os.path.abspath(__file__))
            if not app_dir:
                app_dir = os.getcwd()
            cache_db_path = os.path.join(app_dir, "chat_cache.db")
            self.cache = ChatCache(db_path=cache_db_path)
            self.exports_dir = os.path.join(app_dir, "exports")
            os.makedirs(self.exports_dir, exist_ok=True)
            page.controls.append(ft.Text("Кэш создан", color=ft.Colors.GREEN))
        except Exception as e:
            page.controls.append(ft.Text(f"Ошибка создания кэша: {e}", color=ft.Colors.RED))
            page.update()
            return

        # 3. Инициализация API клиента
        try:
            self.api_client = OpenRouterClient()
            page.controls.append(ft.Text("API клиент создан", color=ft.Colors.GREEN))
        except Exception as e:
            page.controls.append(ft.Text(f"Ошибка API клиента: {e}", color=ft.Colors.RED))
            page.update()
            return

        # 4. Получение списка моделей
        try:
            models = self.api_client.available_models
            if not models:
                raise ValueError("Список моделей пуст")
            page.controls.append(ft.Text(f"Загружено {len(models)} моделей", color=ft.Colors.GREEN))
        except Exception as e:
            page.controls.append(ft.Text(f"Ошибка получения моделей: {e}", color=ft.Colors.RED))
            page.update()
            return

        # 5. Обновление баланса
        try:
            self.update_balance()
            page.controls.append(ft.Text(f"Баланс: {self.balance_text.value}", color=ft.Colors.GREEN))
        except Exception as e:
            page.controls.append(ft.Text(f"Ошибка получения баланса: {e}", color=ft.Colors.RED))
            # не фатально, продолжаем

        page.update()

        # Настройка страницы
        for key, value in AppStyles.PAGE_SETTINGS.items():
            setattr(page, key, value)
        AppStyles.set_window_size(page)

        # Инициализация хранилища
        app_dir = os.path.dirname(os.path.abspath(__file__))
        if not app_dir:
            app_dir = os.getcwd()  # fallback для локального запуска
        cache_db_path = os.path.join(app_dir, "chat_cache.db")
        self.exports_dir = os.path.join(app_dir, "exports")
        os.makedirs(self.exports_dir, exist_ok=True)

        # Инициализация компонентов
        self.cache = ChatCache(db_path=cache_db_path)
        self.analytics = Analytics(self.cache)
        try:
            self.api_client = OpenRouterClient()
        except ValueError as e:
            page.add(ft.Text(f"Ошибка: {e}", color=ft.Colors.RED, size=20))
            page.update()
            return

        # Обновление баланса
        self.update_balance()

        # UI: список моделей
        models = self.api_client.available_models
        self.model_dropdown = ModelSelector(models)

        # История чата
        self.chat_history = ft.ListView(**AppStyles.CHAT_HISTORY)

        # Загрузка предыдущих сообщений
        self.load_chat_history()

        # Поле ввода
        self.message_input = ft.TextField(**AppStyles.MESSAGE_INPUT)

        # Кнопки
        send_button = ft.ElevatedButton(
            on_click=self.send_message_click,
            **AppStyles.SEND_BUTTON
        )
        save_button = ft.ElevatedButton(
            on_click=self.save_dialog,
            **AppStyles.SAVE_BUTTON
        )
        clear_button = ft.ElevatedButton(
            on_click=self.confirm_clear_history,
            **AppStyles.CLEAR_BUTTON
        )
        analytics_button = ft.ElevatedButton(
            on_click=self.show_analytics,
            **AppStyles.ANALYTICS_BUTTON
        )

        input_row = ft.Row([self.message_input, send_button], **AppStyles.INPUT_ROW)
        control_buttons = ft.Row([save_button, analytics_button, clear_button], **AppStyles.CONTROL_BUTTONS_ROW)
        controls_column = ft.Column([input_row, control_buttons], **AppStyles.CONTROLS_COLUMN)

        balance_container = ft.Container(content=self.balance_text, **AppStyles.BALANCE_CONTAINER)
        model_selection = ft.Column([
            self.model_dropdown.search_field,
            self.model_dropdown,
            balance_container
        ], **AppStyles.MODEL_SELECTION_COLUMN)

        main_column = ft.Column([
            model_selection,
            self.chat_history,
            controls_column
        ], **AppStyles.MAIN_COLUMN)

        page.add(main_column)
        self.monitor.get_metrics()
        self.logger.info("App started")

    def load_chat_history(self):
        try:
            history = self.cache.get_chat_history()
            for msg in reversed(history):
                _, model, user_msg, ai_msg, _, _ = msg
                self.chat_history.controls.append(MessageBubble(user_msg, is_user=True))
                self.chat_history.controls.append(MessageBubble(ai_msg, is_user=False))
        except Exception as e:
            self.logger.error(f"Error loading history: {e}")

    def update_balance(self):
        try:
            balance = self.api_client.get_balance()
            self.balance_text.value = f"Баланс: {balance}"
            self.balance_text.color = ft.Colors.GREEN_400
        except Exception as e:
            self.balance_text.value = "Баланс: н/д"
            self.balance_text.color = ft.Colors.RED_400
            self.logger.error(f"Balance error: {e}")

    async def send_message_click(self, e):
        if not self.message_input.value:
            return
        try:
            self.message_input.border_color = ft.Colors.BLUE_400
            e.page.update()

            start_time = time.time()
            user_message = self.message_input.value
            self.message_input.value = ""
            e.page.update()

            self.chat_history.controls.append(MessageBubble(user_message, is_user=True))
            loading = ft.ProgressRing()
            self.chat_history.controls.append(loading)
            e.page.update()

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.api_client.send_message(user_message, self.model_dropdown.value)
            )

            self.chat_history.controls.remove(loading)

            if "error" in response:
                response_text = f"Ошибка: {response['error']}"
                tokens_used = 0
            else:
                response_text = response["choices"][0]["message"]["content"]
                tokens_used = response.get("usage", {}).get("total_tokens", 0)

            self.cache.save_message(
                model=self.model_dropdown.value,
                user_message=user_message,
                ai_response=response_text,
                tokens_used=tokens_used
            )
            self.chat_history.controls.append(MessageBubble(response_text, is_user=False))

            response_time = time.time() - start_time
            self.analytics.track_message(
                model=self.model_dropdown.value,
                message_length=len(user_message),
                response_time=response_time,
                tokens_used=tokens_used
            )
            self.monitor.log_metrics(self.logger)
            e.page.update()

        except Exception as e:
            self.logger.error(f"Send error: {e}")
            show_error_snack(e.page, str(e))
            self.message_input.border_color = ft.Colors.RED_500
            e.page.update()

    async def show_analytics(self, e):
        stats = self.analytics.get_statistics()
        dialog = ft.AlertDialog(
            title=ft.Text("Аналитика"),
            content=ft.Column([
                ft.Text(f"Сообщений: {stats['total_messages']}"),
                ft.Text(f"Токенов: {stats['total_tokens']}"),
                ft.Text(f"Токенов/сообщение: {stats['tokens_per_message']:.2f}"),
                ft.Text(f"Сообщений/мин: {stats['messages_per_minute']:.2f}")
            ]),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: self.close_dialog(dialog, e.page))],
        )
        e.page.overlay.append(dialog)
        dialog.open = True
        e.page.update()

    async def confirm_clear_history(self, e):
        async def clear_confirmed(_):
            self.cache.clear_history()
            self.analytics.clear_data()
            self.chat_history.controls.clear()
            self.close_dialog(dialog, e.page)
            e.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение"),
            content=ft.Text("Удалить всю историю? Это необратимо!"),
            actions=[
                ft.TextButton("Отмена", on_click=lambda ev: self.close_dialog(dialog, e.page)),
                ft.TextButton("Очистить", on_click=clear_confirmed),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        e.page.overlay.append(dialog)
        dialog.open = True
        e.page.update()

    async def save_dialog(self, e):
        try:
            history = self.cache.get_formatted_history()
            filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.exports_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2, default=str)
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Сохранено"),
                content=ft.Column([
                    ft.Text("Файл:"),
                    ft.Text(filepath, selectable=True, weight=ft.FontWeight.BOLD),
                ]),
                actions=[ft.TextButton("OK", on_click=lambda ev: self.close_dialog(dialog, e.page))],
            )
            e.page.overlay.append(dialog)
            dialog.open = True
            e.page.update()
        except Exception as e:
            self.logger.error(f"Save error: {e}")
            show_error_snack(e.page, str(e))

    def close_dialog(self, dialog, page):
        dialog.open = False
        page.update()
        if dialog in page.overlay:
            page.overlay.remove(dialog)


def main(page: ft.Page):
    app = ChatApp()
    # Передаём page в main
    import asyncio
    asyncio.ensure_future(app.main(page))
