from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.domain.repositories.user_repository import UserRepository
from app.modules.users.infrastructure.database.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserModel) -> UserModel:

        self.db.add(user)

        await self.db.commit()

        await self.db.refresh(user)

        return user

    async def get_users(
        self,
        page: int = 1,
        page_size: int = 10,
    ) -> list[UserModel] | None:
        query = select(UserModel).offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(query)

        return list(result.scalars().all())

    async def count_users(self) -> int:
        query = select(func.count()).select_from(UserModel)

        result = await self.db.execute(query)

        return result.scalar_one()

    async def count_active_users(self) -> int:
        query = (
            select(func.count())
            .select_from(UserModel)
            .where(UserModel.is_active.is_(True))
        )

        result = await self.db.execute(query)

        return result.scalar_one()

    async def count_inactive_users(self) -> int:
        query = (
            select(func.count())
            .select_from(UserModel)
            .where(UserModel.is_active.is_(False))
        )

        result = await self.db.execute(query)

        return result.scalar_one()

    async def get_by_id(self, user_id: str) -> UserModel | None:

        query = select(UserModel).where(UserModel.id == user_id)

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.email == email)

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.username == username)

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def delete_user(self, user_id: str) -> None:
        query = select(UserModel).where(UserModel.id == user_id)

        result = await self.db.execute(query)

        user = result.scalar_one_or_none()

        if not user:
            return None

        user.is_active = False

        await self.db.commit()
        await self.db.refresh(user)

    async def update_user(
        self,
        user_id: str,
        update_data: dict[str, object],
    ) -> UserModel | None:
        query = select(UserModel).where(UserModel.id == user_id)

        result = await self.db.execute(query)

        user = result.scalar_one_or_none()

        if not user:
            return None

        for key, value in update_data.items():
            setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)

        return user
