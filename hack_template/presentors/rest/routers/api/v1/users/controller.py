from http import HTTPStatus
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post

from hack_template.domains.entities.users import CreateUser, User, UserId
from hack_template.domains.uow import AbstractUow
from hack_template.domains.use_cases.fetch_user_by_id import FetchUserByID
from hack_template.domains.use_cases.register_user import RegisterUser
from hack_template.presentors.rest.routers.api.v1.users import urls
from hack_template.presentors.rest.routers.api.v1.users.schemas import RegisterUserModel


class UsersController(Controller):
    tags = ["Users"]

    @get(
        operation_id="fetch_user_by_id",
        name="users:detail",
        summary="Fetch user by id",
        path=urls.USER_DETAIL,
        status_code=HTTPStatus.OK,
    )
    @inject
    async def user_detail(
        self,
        user_id: UUID,
        uow: FromDishka[AbstractUow],
        fetch_user_by_id: FromDishka[FetchUserByID],
    ) -> User:
        async with uow(read_only=True):
            return await fetch_user_by_id.execute(input_dto=UserId(user_id))

    @post(
        operation_id="register_user",
        name="users:register",
        summary="Register new user",
        path=urls.USER_REGISTER,
        status_code=HTTPStatus.CREATED,
    )
    @inject
    async def register_user(
        self,
        data: RegisterUserModel,
        uow: FromDishka[AbstractUow],
        register_user: FromDishka[RegisterUser],
    ) -> User:
        async with uow(read_only=False):
            create_user = CreateUser(
                username=data.username,
                email=data.email,
                telegram_id=data.telegram_id,
                password=data.password,
            )
            return await register_user.execute(input_dto=create_user)
