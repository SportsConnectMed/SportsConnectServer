from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.matches.domain.enums.match_status import MatchStatus
from app.modules.matches.domain.repositories.match_repository import MatchRepository


class CancelMatchUseCase:
    def __init__(
        self,
        db: AsyncSession,
        match_repository: MatchRepository,
    ):
        self.db = db

        self.match_repository = match_repository

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

            # Only creator can cancel the match
            if match.creator_id != user_id:
                raise ValueError("Only the match creator can cancel this match")

            # Match already cancelled
            if match.status == MatchStatus.CANCELLED:
                raise ValueError("Match already cancelled")

            # Cancel match
            match.status = MatchStatus.CANCELLED

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
