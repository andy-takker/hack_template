from faststream.rabbit import RabbitBroker
from faststream.security import SASLPlaintext

from hack_template.presentors.amqp.config import RabbitMQConfig


def create_new_broker(config: RabbitMQConfig) -> RabbitBroker:
    return RabbitBroker(
        host=config.host,
        port=config.port,
        security=SASLPlaintext(
            username=config.username,
            password=config.password,
        ),
        virtualhost="/",
    )
