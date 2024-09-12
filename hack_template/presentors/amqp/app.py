from faststream import FastStream

from hack_template.adapters.amqp.broker import create_new_broker
from hack_template.presentors.amqp.config import RabbitMQConfig
from hack_template.presentors.amqp.controllers import AMQPSenderController


def get_amqp_app(config: RabbitMQConfig) -> FastStream:
    broker = create_new_broker(config=config)
    fastsstream_app = FastStream(broker=broker)
    broker.include_router(AMQPSenderController)
    return fastsstream_app
