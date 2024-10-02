from dishka import AnyOf, BaseScope, Provider, Scope, provide

from hack_template.adapters.passgen import Passgen
from hack_template.application.config import SecretConfig
from hack_template.domains.interfaces.adapters.passgen import IPassgen


class AdapterProvider(Provider):
    __config: SecretConfig

    def __init__(
        self,
        config: SecretConfig,
        scope: BaseScope | None = None,
        component: str | None = None,
    ):
        self.__config = config
        super().__init__(scope, component)

    @provide(scope=Scope.APP)
    def passgen(self) -> AnyOf[IPassgen, Passgen]:
        return Passgen(secret=self.__config.secret)
