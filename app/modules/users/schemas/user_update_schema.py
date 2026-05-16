from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl

from app.modules.users.schemas.user_create_schema import UsernameField


class UserUpdateSchema(BaseModel):
    username: UsernameField | None = None

    email: EmailStr | None = None

    # password: PasswordField | None = None -> Later implementation

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
        extra="forbid",
        str_strip_whitespace=True,
    )
