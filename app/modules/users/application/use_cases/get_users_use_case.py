from app.modules.users.domain.repositories.user_repository import (
    UserRepository,
)
from app.modules.users.infrastructure.database.models.user_model import (
    UserModel,
)


class GetUsersUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self) -> list[UserModel]:

        return await self.user_repository.get_users()
