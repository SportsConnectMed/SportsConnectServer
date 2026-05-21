from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.matches.domain.repositories.match_player_repository import (
    MatchPlayerRepository,
)
from app.modules.matches.infrastructure.database.models.match_player_model import (
    MatchPlayerModel,
)


class SQLAlchemyMatchPlayerRepository(MatchPlayerRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        match_player: MatchPlayerModel,
    ) -> MatchPlayerModel:
        self.db.add(match_player)

        await self.db.flush()

        await self.db.refresh(match_player)

        return match_player

    async def delete(self, match_player: MatchPlayerModel):
        await self.db.delete(match_player)

    async def get_by_match_and_user(
        self,
        match_id: str,
        user_id: str,
    ) -> MatchPlayerModel | None:

        statement = select(MatchPlayerModel).where(
            MatchPlayerModel.match_id == match_id,
            MatchPlayerModel.user_id == user_id,
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()
