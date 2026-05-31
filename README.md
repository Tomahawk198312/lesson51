# AI Chat на Flet

Кроссплатформенное приложение для общения с искусственным интеллектом через OpenRouter.ai.  
Поддерживает более 215 языковых моделей, сохраняет историю чата, предоставляет аналитику использования и баланс аккаунта.

## 📁 Структура проекта
lesson51/
├── assets/
│   ├── .env                  # Файл с ключами
│   └── icon.png              # Иконка приложения
├── android/
│   └── manifest.template.xml # Манифест для Android
├── src/
│   ├── api/                  # Клиент OpenRouter API
│   ├── ui/                   # Компоненты интерфейса и стили
│   ├── utils/                # Утилиты (кеш, логгер, аналитика, мониторинг)
│   ├── main.py               # Основное приложение
│   └── main_simple.py        # Упрощённая версия (опционально)
├── build.py                  # Скрипт десктоп-сборки
├── requirements.txt          # Зависимости
├── flet.toml                 # Конфигурация сборки APK
└── README.md


## Требования

- Python 3.9 или выше (рекомендуется 3.13+)
- Для локальной сборки APK: Docker Desktop, JDK 17+, Android SDK
- OpenRouter API ключ (зарегистрируйтесь на [openrouter.ai](https://openrouter.ai))

## Сборка Android APK

### Локальная сборка (требуется Docker)

1. Убедитесь, что Docker Desktop запущен.
2. Настройте переменные окружения `JAVA_HOME` и `ANDROID_HOME`.
3. Убедитесь, что установлены Android SDK platform 34 и build-tools 34.0.0.
4. Запустите сборку:
   ```bash
   flet build apk
   ```
   На вопросы отвечайте:
   - Project name: `lesson51`
   - Package name: `com.example.lesson51`
   - Path to assets: `assets`
   - Minimum Android SDK: `21`
5. APK появится в `build/android/app/build/outputs/apk/release/app-release.apk`.

### Сборка через GitHub Actions

1. Добавьте секрет `OPENROUTER_API_KEY` в настройках репозитория (Settings → Secrets and variables → Actions).
2. Workflow `build-apk.yml` уже настроен. Запустите его вручную (вкладка Actions → Build Android APK → Run workflow).
3. После завершения скачайте артефакт `app-release` (как описано в начале).

## Настройка OpenRouter API

- Зарегистрируйтесь на [OpenRouter.ai](https://openrouter.ai).
- Создайте API ключ.
- В файле `assets/.env` укажите:
  ```
  OPENROUTER_API_KEY=ваш_ключ
  BASE_URL=https://openrouter.ai/api/v1
  ```
- Для локальной разработки этот файл будет использоваться напрямую. При сборке APK содержимое папки `assets` копируется в приложение.

## Использование приложения

- Выберите модель из выпадающего списка (доступен поиск).
- Введите сообщение и нажмите «Отправить».
- История чата сохраняется в локальной базе данных.
- Кнопка «Аналитика» показывает статистику использования.
- Кнопка «Сохранить» экспортирует диалог в JSON во внутреннюю память устройства.
- Баланс OpenRouter отображается в верхней части экрана.