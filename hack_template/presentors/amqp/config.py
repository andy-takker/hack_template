from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, kw_only=True, slots=True)
class RabbitMQConfig:
    host: str = field(default_factory=lambda: environ["APP_RABBITMQ_HOST"])
    port: int = field(default_factory=lambda: int(environ["APP_RABBITMQ_PORT"]))
    username: str = field(default_factory=lambda: environ["APP_RABBITMQ_USER"])
    password: str = field(default_factory=lambda: environ["APP_RABBITMQ_PASSWORD"])
