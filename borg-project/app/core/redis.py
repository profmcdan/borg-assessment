import redis

from .config import settings


def cache():
    return redis.Redis(
        host=settings.redis_server,
        port=settings.redis_port,
        db=settings.redis_db
    )
