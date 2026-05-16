from app.modules.users.domain.repositories.user_repository import (
    UserRepository,
)
from app.modules.users.infrastructure.database.models.user_model import (
    UserModel,
)


class GetUserByIDUseCase:
    def __init__(self, user_repository: UserRepository, user_id: str):
        self.user_repository = user_repository
        self.user_id = user_id

    async def execute(self) -> UserModel:

        return await self.user_repository.get_by_id(self.user_id)
