from hack_template.application.common.exceptions import EntityNotFoundError
from hack_template.domains.entities.users import (
    CreateUser,
    User,
    UserId,
    UserPagination,
    UserPaginationFilter,
)
from hack_template.domains.interfaces.adapters.passgen import IPassgen
from hack_template.domains.interfaces.storages.user import IUserStorage


class UserService:
    __user_storage: IUserStorage
    __passgen: IPassgen

    def __init__(self, user_storage: IUserStorage, passgen: IPassgen) -> None:
        self.__user_storage = user_storage
        self.__passgen = passgen

    async def fetch_user_by_id(self, *, user_id: UserId) -> User:
        user = await self.__user_storage.fetch_user_by_id(user_id=user_id)
        if user is None:
            raise EntityNotFoundError(entity=User, entity_id=user_id)
        return user

    async def create_user(self, *, data: CreateUser) -> User:
        hashed_password = await self.__passgen.hash_password(password=data.password)
        return await self.__user_storage.create_user(
            data=CreateUser(
                username=data.username,
                email=data.email,
                telegram_id=data.telegram_id,
                password=hashed_password,
            )
        )

    async def fetch_user_list(self, *, filter: UserPaginationFilter) -> UserPagination:
        users = await self.__user_storage.fetch_users(filter=filter)
        total = await self.__user_storage.count_users(filter=filter)
        return UserPagination(items=users, total=total)
