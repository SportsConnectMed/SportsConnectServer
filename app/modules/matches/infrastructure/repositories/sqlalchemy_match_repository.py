from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.matches.domain.repositories.match_repository import (
    MatchRepository,
)
from app.modules.matches.infrastructure.database.models.match_model import (
    MatchModel,
)
from app.modules.matches.infrastructure.database.models.match_player_model import (
    MatchPlayerModel,
)


class SQLAlchemyMatchRepository(MatchRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        match: MatchModel,
    ) -> MatchModel:
        self.db.add(match)

        await self.db.flush()

        return match

    async def save(self, match: MatchModel) -> MatchModel:
        self.db.add(match)

        await self.db.flush()

        await self.db.refresh(match)

        return match

    async def get_all(self) -> list[MatchModel]:

        statement = select(MatchModel).options(
            selectinload(MatchModel.players).selectinload(MatchPlayerModel.user)
        )

        result = await self.db.execute(statement)

        return list(result.scalars().all())

    async def get_by_id(
        self,
        match_id: str,
    ) -> MatchModel | None:

        statement = (
            select(MatchModel)
            .where(MatchModel.id == match_id)
            .options(
                selectinload(MatchModel.players).selectinload(MatchPlayerModel.user)
            )
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()
