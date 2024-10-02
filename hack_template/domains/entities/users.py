from collections.abc import Sequence
from dataclasses import dataclass
from typing import NewType
from uuid import UUID

UserId = NewType("UserId", UUID)


@dataclass(frozen=True, slots=True, kw_only=True)
class User:
    id: UserId
    username: str
    email: str | None
    telegram_id: int | None


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUser:
    username: str
    email: str | None
    telegram_id: int | None
    password: str


@dataclass(frozen=True, slots=True, kw_only=True)
class UserPaginationFilter:
    limit: int
    offset: int


@dataclass(frozen=True, slots=True, kw_only=True)
class UserPagination:
    items: Sequence[User]
    total: int
