from abc import abstractmethod
from typing import Protocol


class IPassgen(Protocol):
    @abstractmethod
    async def hash_password(self, *, password: str) -> str:
        raise NotImplementedError
