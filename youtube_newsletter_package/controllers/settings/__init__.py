from .general_settings import GeneralSettings
from .redis_settings import RedisSettings
from .rabbitmq_settings import RabbitMQSettings
from .celery_settings import CelerySettings


class Settings(GeneralSettings, CelerySettings, RedisSettings, RabbitMQSettings):
    pass
