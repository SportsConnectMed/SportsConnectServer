from app.modules.matches.domain.repositories.match_repository import MatchRepository


class GetMatchByIdUseCase:
    def __init__(
        self,
        match_repository: MatchRepository,
    ):
        self.match_repository = match_repository

    async def execute(
        self,
        match_id: str,
    ):

        match = await self.match_repository.get_by_id(match_id)

        if not match:
            raise ValueError("Match not found")

        return match
