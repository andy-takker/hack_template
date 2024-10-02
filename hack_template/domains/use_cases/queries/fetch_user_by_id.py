from hack_template.application.common.use_case import IUseCase
from hack_template.domains.entities.users import User, UserId
from hack_template.domains.services.user import UserService


class FetchUserByID(IUseCase[UserId, User]):
    __user_service: UserService

    def __init__(self, user_service: UserService) -> None:
        self.__user_service = user_service

    async def execute(self, *, input_dto: UserId) -> User:
        return await self.__user_service.fetch_user_by_id(user_id=input_dto)
