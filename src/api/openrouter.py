import os
import requests

from ..utils.logger import AppLogger


class OpenRouterClient:
    def __init__(self):
        self.logger = AppLogger()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("BASE_URL")
        if not self.api_key:
            self.logger.error("OpenRouter API key not found")
            raise ValueError("API key not found in .env")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.logger.info("OpenRouterClient initialized")
        self.available_models = self.get_models()

    def get_models(self):
        try:
            resp = requests.get(f"{self.base_url}/models", headers=self.headers)
            data = resp.json()
            models = [{"id": m["id"], "name": m["name"]} for m in data["data"]]
            self.logger.info(f"Loaded {len(models)} models")
            return models
        except Exception as e:
            self.logger.error(f"Failed to fetch models: {e}")
            return [
                {"id": "deepseek/deepseek-chat", "name": "DeepSeek Chat"},
                {"id": "anthropic/claude-3-haiku", "name": "Claude 3 Haiku"},
                {"id": "openai/gpt-3.5-turbo", "name": "GPT-3.5 Turbo"}
            ]

    def send_message(self, message, model):
        self.logger.debug(f"Sending to {model}")
        data = {
            "model": model,
            "messages": [{"role": "user", "content": message}]
        }
        try:
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data
            )
            resp.raise_for_status()
            self.logger.info("API response received")
            return resp.json()
        except Exception as e:
            self.logger.error(f"API request failed: {e}", exc_info=True)
            return {"error": str(e)}

    def get_balance(self):
        try:
            resp = requests.get(f"{self.base_url}/credits", headers=self.headers)
            data = resp.json().get("data", {})
            total = data.get("total_credits", 0) - data.get("total_usage", 0)
            return f"${total:.2f}"
        except:
            return "Ошибка"
