from pydantic import BaseModel, Field


class RegisterUserModel(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(
        min_length=8,
        max_length=32,
        pattern=r"[A-Za-z\d@$!%*?&]{8,32}",
    )
    email: str | None = Field(
        None, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )
    telegram_id: int | None = Field(None)
