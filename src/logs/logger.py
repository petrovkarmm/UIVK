import logging
import os
from logging.handlers import TimedRotatingFileHandler

from src.settings import BOT_BASE_DIR

log_dir = os.path.join(BOT_BASE_DIR, 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, 'aiogram.log')

bot_logger = logging.getLogger('bot_logger')
bot_logger.setLevel(logging.INFO)

bot_file_handler = TimedRotatingFileHandler(
    filename=log_file_path,
    when='W0',
    interval=1,
    backupCount=4,
    encoding='utf-8'
)
bot_file_handler.setLevel(logging.INFO)

bot_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
bot_file_handler.setFormatter(bot_formatter)

bot_logger.addHandler(bot_file_handler)

logging.getLogger('aiogram').setLevel(logging.WARNING)


async def handler_log(user, state, start_data, dialog_data):
    log_message = (
        f"| Состояние: {state} | start_data: {start_data} | dialog_data: {dialog_data} | User: {user} |"
    )
    bot_logger.info(log_message)
