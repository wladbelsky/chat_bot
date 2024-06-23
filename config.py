from os import getenv

TOKEN = getenv("BOT_TOKEN")

WEB_SERVER_HOST = getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = getenv("WEB_SERVER_PORT")

WEBHOOK_PATH = getenv("WEBHOOK_PATH")
WEBHOOK_SECRET = getenv("WEBHOOK_SECRET")
BASE_WEBHOOK_URL = getenv("BASE_WEBHOOK_URL")
CHAT_GPT_TOKEN = getenv("CHAT_GPT_TOKEN")

DB_CONFIG = {
    'engine': getenv('DB_ENGINE', 'postgresql+asyncpg'),
    'user': getenv('DB_USER'),
    'password': getenv('DB_PASSWORD'),
    'host': getenv('DB_HOST'),
    'port': getenv('DB_PORT'),
    'database': getenv('DB_NAME'),
}

REDIS_SERVER = getenv('REDIS_SERVER')
REDIS_PORT = getenv('REDIS_PORT')
REDIS_PASSWORD = getenv('REDIS_PASSWORD')

MEMORY_TIME = 60*60
OPERATOR_LIST = [
    292143060,
]  # Хардкод, стоит конечно вынести в базу данных
