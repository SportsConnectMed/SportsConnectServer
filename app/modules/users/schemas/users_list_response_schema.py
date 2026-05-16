from pydantic import BaseModel
from app.modules.users.schemas.user_response_schema import UserResponseSchema


class UserListResponseSchema(BaseModel):
    total: int
    active: int
    inactive: int
    users: list[UserResponseSchema]
