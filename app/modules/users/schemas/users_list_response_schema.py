from pydantic import BaseModel

from app.modules.users.schemas.user_response_schema import UserResponseSchema


class UserListResponseSchema(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    active: int
    inactive: int
    users: list[UserResponseSchema]
