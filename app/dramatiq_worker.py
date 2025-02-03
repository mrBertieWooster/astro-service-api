import dramatiq
from dramatiq.brokers.redis import RedisBroker
from app.config import Settings

settings = Settings()

redis_broker = RedisBroker(url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0")
dramatiq.set_broker(redis_broker)