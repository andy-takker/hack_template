from dishka import Provider, Scope, provide

from hack_template.domains.interfaces.adapters.passgen import IPassgen
from hack_template.domains.interfaces.storages.user import IUserStorage
from hack_template.domains.services.user import UserService
from hack_template.domains.use_cases.handlers.register_user import RegisterUser


class DomainProvider(Provider):
    @provide(scope=Scope.APP)
    def user_service(
        self,
        user_storage: IUserStorage,
        passgen: IPassgen,
    ) -> UserService:
        return UserService(user_storage=user_storage, passgen=passgen)

    @provide(scope=Scope.APP)
    def register_user(
        self,
        user_service: UserService,
    ) -> RegisterUser:
        return RegisterUser(user_service=user_service)
