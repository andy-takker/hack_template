import uuid
from typing import NoReturn
from uuid import UUID

from sqlalchemy import CursorResult, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError

from hack_template.adapters.database.tables import UserTable
from hack_template.adapters.database.uow import SqlalchemyUow
from hack_template.application.common.exceptions import (
    DatabaseStorageError,
    DuplicateUsernameError,
)
from hack_template.domains.entities.users import CreateUser, User
from hack_template.domains.users.storage import IUserStorage


class PGUserStorage(IUserStorage):
    __uow: SqlalchemyUow

    def __init__(self, uow: SqlalchemyUow) -> None:
        self.__uow = uow

    async def create_user(self, *, data: CreateUser) -> User:
        stmt = (
            insert(UserTable)
            .values(
                id=uuid.uuid4(),
                username=data.username,
                email=data.email,
                telegram_id=data.telegram_id,
                password=data.password,
            )
            .returning(UserTable)
        )
        try:
            result: CursorResult = await self.__uow.connection.execute(stmt)
        except IntegrityError as e:
            self._raise_error(e)
        user_data = result.mappings().one()
        return User(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"],
            telegram_id=user_data["telegram_id"],
        )

    async def fetch_user_by_id(self, *, user_id: UUID) -> User | None:
        query = select(UserTable).where(UserTable.id == user_id)

        result: CursorResult = await self.__uow.connection.execute(query)
        user = result.mappings().first()
        if user is None:
            return None
        return User(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            telegram_id=user["telegram_id"],
        )

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]

        if constraint == "uq__users__username":
            raise DuplicateUsernameError from e

        raise DatabaseStorageError from e
