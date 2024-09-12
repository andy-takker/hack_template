from hack_template.application.common.exceptions import EntityNotFoundError
from hack_template.application.common.use_case import IUseCase
from hack_template.domains.entities.users import User, UserId
from hack_template.domains.users.storage import IUserStorage


class FetchUserByID(IUseCase[UserId, User]):
    def __init__(self, user_storage: IUserStorage) -> None:
        self.user_storage = user_storage

    async def execute(self, *, input_dto: UserId) -> User:
        user = await self.user_storage.fetch_user_by_id(user_id=input_dto)
        if user is None:
            raise EntityNotFoundError(entity=User, entity_id=input_dto)
        return user
