from app.modules.matches.domain.repositories.match_repository import MatchRepository


class GetMatchesUseCase:
    def __init__(
        self,
        match_repository: MatchRepository,
    ):
        self.match_repository = match_repository

    async def execute(self):

        return await self.match_repository.get_all()
