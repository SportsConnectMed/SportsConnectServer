from abc import ABC, abstractmethod
from typing import Any

from app.modules.users.infrastructure.database.models.user_model import UserModel


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: UserModel) -> UserModel: ...

    @abstractmethod
    async def get_users(
        self,
        page: int = 1,
        page_size: int = 10,
    ) -> list[UserModel] | None: ...

    @abstractmethod
    async def count_users(self) -> int: ...

    @abstractmethod
    async def count_active_users(self) -> int: ...

    @abstractmethod
    async def count_inactive_users(self) -> int: ...

    @abstractmethod
    async def get_by_id(self, user_id: str) -> UserModel | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserModel | None: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> UserModel | None: ...

    @abstractmethod
    async def update_user(
        self,
        user_id: str,
        update_data: dict[str, Any],
    ) -> UserModel | None: ...

    @abstractmethod
    async def delete_user(self, user_id: str) -> None: ...
