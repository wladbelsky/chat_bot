import redis.asyncio as redis
from config import REDIS_PORT, REDIS_SERVER, REDIS_PASSWORD


class Redis:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection_pool = redis.ConnectionPool(
                host=REDIS_SERVER,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                decode_responses=True
            )
        return cls._instance

    def get_connection(self):
        return redis.Redis.from_pool(self._connection_pool)
