import flet as ft

class AppStyles:
    PAGE_SETTINGS = {
        "title": "AI Chat",
        "vertical_alignment": ft.MainAxisAlignment.START,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
        "padding": ft.padding.only(top=32, left=10, right=10, bottom=10),
        "bgcolor": ft.Colors.GREY_900,
        "theme_mode": ft.ThemeMode.DARK,
    }
    CHAT_HISTORY = {
        "expand": True,
        "spacing": 10,
        "auto_scroll": True,
        "padding": 10,
    }
    MESSAGE_INPUT = {
        "expand": True,
        "height": 56,
        "multiline": False,
        "text_size": 16,
        "color": ft.Colors.WHITE,
        "bgcolor": ft.Colors.GREY_800,
        "border_color": ft.Colors.BLUE_400,
        "cursor_color": ft.Colors.WHITE,
        "content_padding": ft.padding.symmetric(horizontal=12, vertical=14),
        "border_radius": 8,
        "hint_text": "Введите сообщение здесь...",
        "shift_enter": True,
    }
    SEND_BUTTON = {
        "content": ft.Row([
            ft.Icon(ft.Icons.SEND, color=ft.Colors.WHITE, size=18),
            ft.Text("Отпр.", color=ft.Colors.WHITE, size=14),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
        "style": ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, padding=10),
        "tooltip": "Отправить сообщение",
        "height": 48,
        "width": 82,
    }
    SAVE_BUTTON = {
        "content": ft.Row([
            ft.Icon(ft.Icons.SAVE, color=ft.Colors.WHITE, size=16),
            ft.Text("Сохранить", color=ft.Colors.WHITE, size=13),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
        "style": ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, padding=8),
        "tooltip": "Сохранить диалог в файл",
        "width": 110,
        "height": 42,
    }
    CLEAR_BUTTON = {
        "content": ft.Row([
            ft.Icon(ft.Icons.DELETE, color=ft.Colors.WHITE, size=16),
            ft.Text("Очистить", color=ft.Colors.WHITE, size=13),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
        "style": ft.ButtonStyle(bgcolor=ft.Colors.RED_700, padding=8),
        "tooltip": "Очистить историю чата",
        "width": 110,
        "height": 42,
    }
    ANALYTICS_BUTTON = {
        "content": ft.Row([
            ft.Icon(ft.Icons.ANALYTICS, color=ft.Colors.WHITE, size=16),
            ft.Text("Аналитика", color=ft.Colors.WHITE, size=13),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
        "style": ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700, padding=8),
        "tooltip": "Показать аналитику",
        "width": 110,
        "height": 42,
    }
    INPUT_ROW = {
        "spacing": 8,
        "alignment": ft.MainAxisAlignment.CENTER,
    }
    CONTROL_BUTTONS_ROW = {
        "spacing": 10,
        "alignment": ft.MainAxisAlignment.CENTER,
        "wrap": True,
    }
    CONTROLS_COLUMN = {
        "spacing": 12,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    }
    MAIN_COLUMN = {
        "expand": True,
        "spacing": 10,
        "alignment": ft.MainAxisAlignment.START,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    }
    MODEL_SEARCH_FIELD = {
        "expand": True,
        "border_radius": 8,
        "bgcolor": ft.Colors.GREY_900,
        "border_color": ft.Colors.GREY_700,
        "color": ft.Colors.WHITE,
        "content_padding": 10,
        "cursor_color": ft.Colors.WHITE,
        "focused_border_color": ft.Colors.BLUE_400,
        "focused_bgcolor": ft.Colors.GREY_800,
        "hint_style": ft.TextStyle(color=ft.Colors.GREY_400, size=14),
        "prefix_icon": ft.Icons.SEARCH,
        "height": 45,
    }
    MODEL_DROPDOWN = {
        "expand": True,
        "height": 45,
        "border_radius": 8,
        "bgcolor": ft.Colors.GREY_900,
        "border_color": ft.Colors.GREY_700,
        "color": ft.Colors.WHITE,
        "content_padding": 10,
        "focused_border_color": ft.Colors.BLUE_400,
        "focused_bgcolor": ft.Colors.GREY_800,
    }
    MODEL_SELECTION_COLUMN = {
        "spacing": 10,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    }
    BALANCE_TEXT = {
        "size": 16,
        "color": ft.Colors.GREEN_400,
        "weight": ft.FontWeight.BOLD,
    }
    BALANCE_CONTAINER = {
        "padding": 10,
        "bgcolor": ft.Colors.GREY_900,
        "border_radius": 8,
        "border": ft.border.Border(
            top=ft.border.BorderSide(1, ft.Colors.GREY_700),
            bottom=ft.border.BorderSide(1, ft.Colors.GREY_700),
            left=ft.border.BorderSide(1, ft.Colors.GREY_700),
            right=ft.border.BorderSide(1, ft.Colors.GREY_700),
        ),
    }

    @staticmethod
    def set_window_size(page: ft.Page):
        try:
            page.window.width = 600
            page.window.height = 800
            page.window.resizable = False
        except Exception:
            pass
