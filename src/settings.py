import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEBUG = True

bot_test_token = os.getenv("BOT_TEST_TOKEN")
bot_token = os.getenv("BOT_TOKEN")
redis_connect_url = os.getenv("REDIS_CONNECT_URL")
super_admins = [i.strip() for i in os.getenv("MAIN_ADMIN_TELEGRAM_IDS", "").split(",") if i.strip()]

BOT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
