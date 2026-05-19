from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.matches.domain.repositories.match_repository import (
    MatchRepository,
)
from app.modules.matches.infrastructure.database.models.match_model import (
    MatchModel,
)


class SQLAlchemyMatchRepository(MatchRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        match: MatchModel,
    ) -> MatchModel:
        self.db.add(match)

        await self.db.commit()

        await self.db.refresh(match)

        return match

    async def get_by_id(
        self,
        match_id: str,
    ) -> MatchModel | None:
        result = await self.db.execute(
            select(MatchModel).where(MatchModel.id == match_id)
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
    ) -> list[MatchModel]:
        result = await self.db.execute(select(MatchModel))

        return list(result.scalars().all())
