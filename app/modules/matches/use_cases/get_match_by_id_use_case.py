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
        current_user_id: str | None = None,
    ):

        match = await self.match_repository.get_by_id(match_id)

        if not match:
            raise ValueError("Match not found")

        if current_user_id is not None:
            match.is_joined = self._is_user_joined(match, current_user_id)

        return match

    @staticmethod
    def _is_user_joined(match, current_user_id: str) -> bool:
        return any(player.user_id == current_user_id for player in match.players)
