from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.matches.domain.enums.match_status import MatchStatus
from app.modules.matches.domain.repositories.match_player_repository import (
    MatchPlayerRepository,
)
from app.modules.matches.domain.repositories.match_repository import MatchRepository


class KickPlayerUseCase:
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
        owner_id: str,
        kicked_user_id: str,
    ):

        try:
            match = await self.match_repository.get_by_id(match_id)

            if not match:
                raise ValueError("Match not found")

            if match.creator_id != owner_id:
                raise ValueError("Only the owner can kick players")

            if kicked_user_id == owner_id:
                raise ValueError("Owner cannot kick himself")

            match_player = await self.match_player_repository.get_by_match_and_user(
                match_id=match_id,
                user_id=kicked_user_id,
            )

            if not match_player:
                raise ValueError("User is not in this match")

            await self.match_player_repository.delete(match_player)

            match.current_players -= 1

            if (
                match.status == MatchStatus.FULL
                and match.current_players < match.max_players
            ):
                match.status = MatchStatus.OPEN

            await self.match_repository.save(match)

            await self.db.commit()

            return match

        except Exception:
            await self.db.rollback()

            raise
