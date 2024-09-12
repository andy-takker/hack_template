from hack_template.application.common.use_case import IUseCase
from hack_template.domains.entities.users import CreateUser, User
from hack_template.domains.interfaces.passgen import IPassgen
from hack_template.domains.users.storage import IUserStorage


class RegisterUser(IUseCase[CreateUser, User]):
    def __init__(self, user_storage: IUserStorage, passgen: IPassgen) -> None:
        self.user_storage = user_storage
        self.passgen = passgen

    async def execute(self, *, input_dto: CreateUser) -> User:
        hashed_password = await self.passgen.hash_password(password=input_dto.password)
        user = await self.user_storage.create_user(
            data=CreateUser(
                username=input_dto.username,
                email=input_dto.email,
                telegram_id=input_dto.telegram_id,
                password=hashed_password,
            )
        )
        return user
