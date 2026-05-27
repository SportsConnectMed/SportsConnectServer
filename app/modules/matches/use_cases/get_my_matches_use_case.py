from app.modules.matches.domain.repositories.match_repository import MatchRepository


class GetMyMatchesUseCase:
    def __init__(
        self,
        match_repository: MatchRepository,
    ):
        self.match_repository = match_repository

    async def execute(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 10,
    ):

        matches = await self.match_repository.get_my_matches(
            user_id=user_id,
            page=page,
            page_size=page_size,
        )

        total = await self.match_repository.count_my_matches(user_id=user_id)

        return {
            "matches": matches,
            "total": total,
        }
