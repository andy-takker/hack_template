import hashlib

from hack_template.domains.interfaces.adapters.passgen import IPassgen


class Passgen(IPassgen):
    __secret: bytes

    def __init__(self, *, secret: str) -> None:
        self.__secret = secret.encode()

    async def hash_password(self, *, password: str) -> str:
        return hashlib.sha512(password.encode() + self.__secret).hexdigest()
