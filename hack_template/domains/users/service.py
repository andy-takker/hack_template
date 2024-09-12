from hack_template.application.common.exceptions import EntityNotFoundError
from hack_template.domains.entities.users import User, UserId
from hack_template.domains.users.storage import IUserStorage


class UserService:
    __user_storage: IUserStorage

    def __init__(self, user_storage: IUserStorage) -> None:
        self.__user_storage = user_storage

    async def fetch_user_by_id(self, *, user_id: UserId) -> User:
        user = await self.__user_storage.fetch_user_by_id(user_id=user_id)
        if user is None:
            raise EntityNotFoundError(entity=User, entity_id=user_id)
        return user
