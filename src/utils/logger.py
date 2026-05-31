import logging
import os
from datetime import datetime

class AppLogger:
    def __init__(self):
        self.logs_dir = "logs"
        os.makedirs(self.logs_dir, exist_ok=True)
        log_file = os.path.join(self.logs_dir, f"chat_{datetime.now().strftime('%Y-%m-%d')}.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger = logging.getLogger('ChatApp')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, msg): self.logger.info(msg)
    def error(self, msg, exc_info=None): self.logger.error(msg, exc_info=exc_info)
    def debug(self, msg): self.logger.debug(msg)
    def warning(self, msg): self.logger.warning(msg)