from hack_template.application.common.use_case import IUseCase
from hack_template.domains.entities.users import CreateUser, User
from hack_template.domains.services.user import UserService


class RegisterUser(IUseCase[CreateUser, User]):
    __user_service: UserService

    def __init__(self, user_service: UserService) -> None:
        self.__user_service = user_service

    async def execute(self, *, input_dto: CreateUser) -> User:
        return await self.__user_service.create_user(data=input_dto)
