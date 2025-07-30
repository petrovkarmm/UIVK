import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEBUG = True

bot_test_token = os.getenv("BOT_TEST_TOKEN")

bot_token = os.getenv("BOT_TOKEN")
redis_connect_url = os.getenv("REDIS_CONNECT_URL")
pyrus_login = os.getenv('PYRUS_LOGIN')
pyrus_security_key = os.getenv('PYRUS_SECURITY_KEY')
pyrus_standard_url = 'https://api.pyrus.com/v4'
admin_panel_password = os.getenv("ADMIN_PANEL_PASSWORD")

BOT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
