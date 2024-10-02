from hack_template.application.common.use_case import IUseCase
from hack_template.domains.entities.users import UserPagination, UserPaginationFilter
from hack_template.domains.services.user import UserService


class FetchUserList(IUseCase[UserPaginationFilter, UserPagination]):
    __user_service: UserService

    def __init__(self, user_service: UserService) -> None:
        self.__user_service = user_service

    async def execute(self, *, input_dto: UserPaginationFilter) -> UserPagination:
        return await self.__user_service.fetch_user_list(filter=input_dto)
