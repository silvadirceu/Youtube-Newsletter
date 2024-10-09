from youtube_newsletter_package import CeleryClient, RedisClient

def get_redis():
    """
    Redis client.
    """
    return RedisClient()

def get_celery():
    """
    Celery client.
    """
    return CeleryClient("youtube-newsletter").app