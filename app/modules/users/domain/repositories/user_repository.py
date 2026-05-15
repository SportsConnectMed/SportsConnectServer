from abc import ABC, abstractmethod
from typing import List

from app.modules.users.infrastructure.database.models.user_model import UserModel


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: UserModel) -> UserModel: ...

    @abstractmethod
    async def get_users(self) -> List[UserModel] | None: ...

    @abstractmethod
    async def get_by_id(self, user_id: str) -> UserModel | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserModel | None: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> UserModel | None: ...
