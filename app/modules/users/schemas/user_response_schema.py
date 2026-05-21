from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserResponseSchema(BaseModel):
    id: str
    username: str
    email: str

    full_name: str | None
    city: str | None
    avatar_url: str | None

    is_active: bool
    is_verified: bool

    role: str

    favorite_sport: str | None
    skill_level: str | None
    position: str | None
    bio: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
