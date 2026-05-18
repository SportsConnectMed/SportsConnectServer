from app.core.security import hash_password
from app.modules.users.domain.enums.user_role import UserRole
from app.modules.users.domain.repositories.user_repository import (
    UserRepository,
)
from app.modules.users.infrastructure.database.models.user_model import (
    UserModel,
)
from app.modules.users.schemas.user_create_schema import (
    UserCreateSchema,
)


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, data: UserCreateSchema) -> UserModel:

        existing_email = await self.user_repository.get_by_email(data.email)

        if existing_email:
            raise ValueError("Email already exists")

        existing_username = await self.user_repository.get_by_username(data.username)

        if existing_username:
            raise ValueError("Username already exsists")

        user_data = data.model_dump(exclude={"password", "avatar_url"})

        user = UserModel(
            **user_data,
            hashed_password=hash_password(data.password),
            role=UserRole.USER,
            avatar_url=(str(data.avatar_url) if data.avatar_url else None),
        )

        return await self.user_repository.create(user)
