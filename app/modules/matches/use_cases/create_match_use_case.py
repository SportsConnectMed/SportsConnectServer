from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.matches.domain.repositories.match_player_repository import (
    MatchPlayerRepository,
)
from app.modules.matches.domain.repositories.match_repository import (
    MatchRepository,
)
from app.modules.matches.infrastructure.database.models.match_model import (
    MatchModel,
)
from app.modules.matches.infrastructure.database.models.match_player_model import (
    MatchPlayerModel,
)
from app.modules.matches.schemas.match_create_schema import (
    MatchCreateSchema,
)


class CreateMatchUseCase:
    def __init__(
        self,
        db: AsyncSession,
        match_repository: MatchRepository,
        match_player_repository: MatchPlayerRepository,
    ):
        self.db = db
        self.match_repository = match_repository

        self.match_player_repository = match_player_repository

    async def execute(
        self,
        data: MatchCreateSchema,
        creator_id: str,
    ) -> MatchModel:

        try:
            match = MatchModel(
                title=data.title,
                description=data.description,
                sport=data.sport,
                skill_level=data.skill_level,
                location=data.location,
                max_players=data.max_players,
                scheduled_at=data.scheduled_at,
                creator_id=creator_id,
            )

            created_match = await self.match_repository.create(match)

            match_player = MatchPlayerModel(
                match_id=created_match.id,
                user_id=creator_id,
            )

            await self.match_player_repository.create(match_player)

            await self.db.commit()

            return created_match

        except Exception:
            await self.db.rollback()
            raise
