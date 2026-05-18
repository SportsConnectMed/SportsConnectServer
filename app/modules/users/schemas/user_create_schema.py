from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
)

from app.modules.users.domain.enums.skill_level import SkillLevel
from app.modules.users.domain.enums.sport_type import SportType

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

    favorite_sport: SportType | None = None

    skill_level: SkillLevel | None = None

    position: Annotated[str | None, Field(max_length=100)] = None

    bio: Annotated[str | None, Field(max_length=500)] = None

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )
