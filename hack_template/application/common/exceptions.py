from typing import Any


class HackTemplateException(Exception):
    pass


class EntityNotFoundError(HackTemplateException):
    def __init__(self, entity: type, entity_id: Any) -> None:
        self.message = f"{entity.__name__} with id {entity_id} not found"
        super().__init__(self.message)


class DatabaseStorageError(HackTemplateException):
    pass


class DuplicateUsernameError(DatabaseStorageError):
    def __init__(self, message: str = "Username already exists") -> None:
        self.message = message
        super().__init__(self.message)
