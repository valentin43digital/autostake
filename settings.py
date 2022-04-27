import os
from dotenv import dotenv_values

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
config = dotenv_values(dotenv_path)
ACCOUNT_ADDRESS = config["ACCOUNT_ADDRESS"]
BOT_TOKEN = config["BOT_TOKEN"]

WEBHOOK_HOST = config["WEBHOOK_HOST"]
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = config["WEBAPP_HOST"]
WEBAPP_PORT = config["WEBAPP_PORT"]
