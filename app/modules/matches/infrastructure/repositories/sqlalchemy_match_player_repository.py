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

        await self.db.commit()

        await self.db.refresh(match_player)

        return match_player
