import logging
from contextvars import ContextVar
from typing import Any, Self

from asyncpg.transaction import Transaction
from hasql.asyncsqlalchemy import PoolManager
from hasql.base import PoolAcquireContext
from sqlalchemy.ext.asyncio import AsyncConnection

from hack_template.domains.uow import AbstractUow

log = logging.getLogger(__name__)


class SqlalchemyUow(AbstractUow):
    pool_manager: PoolManager

    read_only: ContextVar[bool] = ContextVar("read_only", default=True)
    transaction: ContextVar[Transaction] = ContextVar("transaction")
    _ctx: ContextVar[PoolAcquireContext] = ContextVar("ctx")
    _connection: ContextVar[AsyncConnection] = ContextVar("connection")

    def __init__(self, *, pool_manager: PoolManager) -> None:
        self.pool_manager = pool_manager

    def __call__(self, *, read_only: bool = False) -> Self:
        self.read_only.set(read_only)
        return self

    async def commit(self) -> None:
        if not self.read_only.get():
            await self.transaction.get().commit()

    async def rollback(self) -> None:
        if not self.read_only.get():
            await self.transaction.get().rollback()

    async def create_transaction(self) -> None:
        read_only = self.read_only.get()
        ctx = self.pool_manager.acquire(read_only=read_only)
        conn: AsyncConnection = await ctx.__aenter__()
        self._connection.set(conn)
        self._ctx.set(ctx)
        if not read_only:
            transaction = await conn.begin()
            self.transaction.set(transaction)

    async def close_transaction(self, *exc: Any) -> None:
        if not self.read_only.get():
            await self.transaction.get().__aexit__(*exc)
        await self._connection.get().close()
        await self._ctx.get().__aexit__(*exc)

    @property
    def connection(self) -> AsyncConnection:
        return self._connection.get()
