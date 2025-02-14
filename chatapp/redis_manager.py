import redis
from functools import lru_cache
from django.conf import settings

@lru_cache(maxsize=1)
def get_redis_client():
    """Returns a cached Redis client instance."""
    redis_config = settings.CHANNEL_LAYERS['default']['CONFIG']['hosts'][0]
    
    # Parse connection details from config
    redis_parts = redis_config.replace('redis://', '').split('@')
    password = redis_parts[0].replace(':', '') if len(redis_parts) > 1 else ''
    host_port = redis_parts[-1]
    host, port = host_port.split(':')
    
    # Create Redis client with best practices
    return redis.Redis(
        host=host,
        port=int(port),
        password=password,
        db=0,
        decode_responses=True,
        socket_timeout=2,
        socket_connect_timeout=2,
        retry_on_timeout=True,
        max_connections=10
    )

def update_user_status(username, status, expire=3600):
    """Update user's online status with expiration."""
    client = get_redis_client()
    key = f"user_status:{username}"
    
    with client.pipeline() as pipe:
        pipe.set(key, status)
        pipe.expire(key, expire)
        pipe.execute()

def get_user_status(username):
    """Gets a user's online status, returns 'offline' if not found."""
    key = f"user_status:{username}"
    return get_redis_client().get(key) or 'offline' 