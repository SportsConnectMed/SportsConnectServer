from app.modules.users.domain.repositories.user_repository import (
    UserRepository,
)
from app.modules.users.infrastructure.database.models.user_model import (
    UserModel,
)


class GetUsersUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(
        self,
        page: int = 1,
        page_size: int = 10,
    ) -> dict[str, int | list[UserModel]]:

        users = await self.user_repository.get_users(
            page=page,
            page_size=page_size,
        )

        total = await self.user_repository.count_users()

        active = await self.user_repository.count_active_users()

        inactive = await self.user_repository.count_inactive_users()

        return {
            "users": users,
            "total": total,
            "active": active,
            "inactive": inactive,
        }
