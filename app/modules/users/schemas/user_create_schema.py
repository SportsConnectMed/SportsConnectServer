from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
)

UsernameField = Annotated[
    str,
    Field(min_length=3, max_length=30),
]

PasswordField = Annotated[
    str,
    Field(min_length=8, max_length=128),
]


class UserCreateSchema(BaseModel):
    username: UsernameField

    email: EmailStr

    password: PasswordField

    full_name: Annotated[
        str | None,
        Field(max_length=100),
    ] = None

    city: Annotated[
        str | None,
        Field(max_length=100),
    ] = None

    avatar_url: HttpUrl | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )
