from app.modules.users.domain.repositories.user_repository import (
    UserRepository,
)
from app.modules.users.infrastructure.database.models.user_model import (
    UserModel,
)
from app.modules.users.schemas.user_update_schema import UserUpdateSchema


class UpdateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        user_id: str,
        update_data: UserUpdateSchema,
    ):
        self.user_repository = user_repository
        self.user_id = user_id
        self.update_data = update_data

    async def execute(self) -> UserModel:

        current_user = await self.user_repository.get_by_id(self.user_id)

        if not current_user:
            raise ValueError("User not found")

        if (
            "email" in self.update_data.model_fields_set
            and self.update_data.email is None
        ):
            raise ValueError("Email cannot be null")

        if (
            "username" in self.update_data.model_fields_set
            and self.update_data.username is None
        ):
            raise ValueError("Username cannot be null")

        if self.update_data.email is not None:
            existing_email = await self.user_repository.get_by_email(
                self.update_data.email
            )

            if existing_email and existing_email.id != self.user_id:
                raise ValueError("Email already exists")

        if self.update_data.username is not None:
            existing_username = await self.user_repository.get_by_username(
                self.update_data.username
            )

            if existing_username and existing_username.id != self.user_id:
                raise ValueError("Username already exsists")

        update_payload = self.update_data.model_dump(exclude_unset=True)

        return await self.user_repository.update_user(self.user_id, update_payload)
