import logging
from collections.abc import Sequence

from aiomisc.service.uvicorn import UvicornApplication, UvicornService
from dishka import AsyncContainer, make_async_container
from dishka.integrations.litestar import setup_dishka
from litestar import Controller, Litestar
from litestar.types import ExceptionHandlersMap

from hack_template.adapters.database.di import DatabaseProvider
from hack_template.adapters.di import AdapterProvider
from hack_template.application.common.exceptions import (
    DuplicateUsernameError,
    EntityNotFoundError,
)
from hack_template.domains.di import DomainProvider
from hack_template.presentors.rest.config import RestConfig
from hack_template.presentors.rest.cors import get_cors_config
from hack_template.presentors.rest.docs import get_openapi_config
from hack_template.presentors.rest.handlers import (
    entity_conflict_handler,
    entity_not_found_handler,
)
from hack_template.presentors.rest.routers.api.v1.users.controller import (
    UsersController,
)

log = logging.getLogger(__name__)


class RestService(UvicornService):
    ROUTE_HANDLERS: Sequence[type[Controller]] = (UsersController,)

    EXCEPTION_HANDLERS: ExceptionHandlersMap = {
        EntityNotFoundError: entity_not_found_handler,
        DuplicateUsernameError: entity_conflict_handler,
    }

    __required__ = ("config",)

    config: RestConfig
    _container: AsyncContainer

    async def create_application(self) -> UvicornApplication:
        log.info("Creating app")
        self.setup_container()
        app = Litestar(
            debug=self.config.app.debug,
            openapi_config=get_openapi_config(config=self.config),
            cors_config=get_cors_config(config=self.config),
            exception_handlers=self.EXCEPTION_HANDLERS,
            middleware=[],
            route_handlers=self.ROUTE_HANDLERS,
        )
        setup_dishka(container=self._container, app=app)
        return app

    async def stop(self, exception: Exception | None = None) -> None:
        await self._container.close(exception=exception)

    def setup_container(self) -> None:
        self._container = make_async_container(
            DomainProvider(),
            DatabaseProvider(self.config.database),
            AdapterProvider(self.config.secret),
        )
