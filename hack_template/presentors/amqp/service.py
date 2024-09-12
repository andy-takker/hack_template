from typing import Any

from aiomisc import Service
from dishka import AsyncContainer, make_async_container

from hack_template.presentors.amqp.app import get_amqp_app
from hack_template.presentors.amqp.config import RabbitMQConfig


class AMQPService(Service):
    __required__ = ("config",)

    config: RabbitMQConfig
    _container: AsyncContainer

    async def start(self) -> None:
        app = get_amqp_app(config=self.config)
        self.setup_container()
        self.start_event.set()
        await app.run()

    async def stop(self, exception: Exception | None = None) -> Any:
        await self._container.close()

    def setup_container(self) -> None:
        self._container = make_async_container()
