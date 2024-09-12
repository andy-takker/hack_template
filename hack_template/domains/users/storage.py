from abc import abstractmethod
from typing import Protocol

from hack_template.domains.entities.users import CreateUser, User, UserId


class IUserStorage(Protocol):
    @abstractmethod
    async def fetch_user_by_id(self, *, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, *, data: CreateUser) -> User:
        raise NotImplementedError
