from dishka import Provider, Scope, provide

from hack_template.domains.interfaces.passgen import IPassgen
from hack_template.domains.use_cases.register_user import RegisterUser
from hack_template.domains.users.service import UserService
from hack_template.domains.users.storage import IUserStorage


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_service(
        self,
        user_storage: IUserStorage,
    ) -> UserService:
        return UserService(user_storage=user_storage)

    @provide(scope=Scope.APP)
    def register_user(
        self, user_storage: IUserStorage, passgen: IPassgen
    ) -> RegisterUser:
        return RegisterUser(user_storage=user_storage, passgen=passgen)
