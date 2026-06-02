from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.matches.domain.enums.match_status import MatchStatus
from app.modules.matches.domain.repositories.match_player_repository import (
    MatchPlayerRepository,
)
from app.modules.matches.domain.repositories.match_repository import MatchRepository
from app.modules.matches.infrastructure.database.models.match_player_model import (
    MatchPlayerModel,
)


class JoinMatchUseCase:
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
        match_id: str,
        user_id: str,
    ):
        try:
            match = await self.match_repository.get_by_id(match_id)

            if not match:
                raise ValueError("Match not found")

            if match.status != MatchStatus.OPEN:
                raise ValueError("Match is not open")

            if match.current_players >= match.max_players:
                raise ValueError("Match is full")

            existing_player = await self.match_player_repository.get_by_match_and_user(
                match_id=match_id,
                user_id=user_id,
            )

            if existing_player:
                raise ValueError("This user already joined")

            match_player = MatchPlayerModel(
                match_id=match.id,
                user_id=user_id,
            )

            await self.match_player_repository.create(match_player)

            match.current_players += 1

            if match.current_players >= match.max_players:
                match.status = MatchStatus.FULL

            await self.match_repository.save(match)

            await self.db.commit()

            match.is_joined = True

            return match

        except ValueError as error:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            )

        except Exception:
            await self.db.rollback()
            raise
