from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.matches.domain.enums.match_status import MatchStatus
from app.modules.matches.domain.repositories.match_player_repository import (
    MatchPlayerRepository,
)
from app.modules.matches.domain.repositories.match_repository import MatchRepository


class LeaveMatchUseCase:
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

            # Match does not exist
            if not match:
                raise ValueError("Match not found")

            # Verify if the user is actually inside the match
            existing_player = await self.match_player_repository.get_by_match_and_user(
                match_id=match_id,
                user_id=user_id,
            )

            # User cannot leave a match he never joined
            if not existing_player:
                raise ValueError("This user is not part of this match")

            # Remove player from pivot table
            await self.match_player_repository.delete(existing_player)

            # Decrease current players
            match.current_players -= 1

            # If nobody remains in the match
            # the match should be cancelled
            if match.current_players <= 0:
                match.status = MatchStatus.CANCELLED

            # If the match was previously full
            # and now has available slots again
            elif match.status == MatchStatus.FULL:
                match.status = MatchStatus.OPEN

            # Save changes
            await self.match_repository.save(match)

            await self.db.commit()

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
