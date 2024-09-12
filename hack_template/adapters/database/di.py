from collections.abc import AsyncIterator

from dishka import AnyOf, BaseScope, Provider, Scope, provide
from hasql.asyncsqlalchemy import PoolManager

from hack_template.adapters.database.config import DatabaseConfig
from hack_template.adapters.database.storages.users import PGUserStorage
from hack_template.adapters.database.uow import SqlalchemyUow
from hack_template.adapters.database.utils import create_pool
from hack_template.domains.uow import AbstractUow
from hack_template.domains.users.storage import IUserStorage


class DatabaseProvider(Provider):
    _config: DatabaseConfig

    def __init__(
        self,
        config: DatabaseConfig,
        scope: BaseScope | None = None,
        component: str | None = None,
    ):
        self._config = config
        super().__init__(scope=scope, component=component)

    @provide(scope=Scope.APP)
    async def pool_manager(self) -> AsyncIterator[PoolManager]:
        pool_manager = await create_pool(
            dsn=self._config.dsn,
            pool_size=self._config.pool_size,
            pool_timeout=self._config.pool_timeout,
            replicas_count=self._config.replicas,
        )
        yield pool_manager
        await pool_manager.close()

    @provide(scope=Scope.APP)
    def uow(self, pool_manager: PoolManager) -> AnyOf[SqlalchemyUow, AbstractUow]:
        return SqlalchemyUow(pool_manager=pool_manager)

    @provide(scope=Scope.APP)
    def user_storage(self, uow: SqlalchemyUow) -> IUserStorage:
        return PGUserStorage(uow=uow)
