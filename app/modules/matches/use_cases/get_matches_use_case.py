from datetime import date

from app.common.enums.skill_level import SkillLevel
from app.common.enums.sport_type import SportType
from app.modules.matches.domain.enums.match_status import MatchStatus
from app.modules.matches.domain.repositories.match_repository import MatchRepository


class GetMatchesUseCase:
    def __init__(
        self,
        match_repository: MatchRepository,
    ):
        self.match_repository = match_repository

    async def execute(
        self,
        sport: SportType | None = None,
        skill_level: SkillLevel | None = None,
        status: MatchStatus | None = None,
        current_players: int | None = None,
        startdate: date | None = None,
        enddate: date | None = None,
        start_hour: int | None = None,
        end_hour: int | None = None,
        location: str | None = None,
        page: int = 1,
        page_size: int = 10,
        current_user_id: str | None = None,
    ):

        matches = await self.match_repository.get_all(
            sport=sport,
            skill_level=skill_level,
            status=status,
            current_players=current_players,
            startdate=startdate,
            enddate=enddate,
            start_hour=start_hour,
            end_hour=end_hour,
            location=location,
            page=page,
            page_size=page_size,
        )

        if current_user_id is not None:
            for match in matches:
                match.is_joined = self._is_user_joined(match, current_user_id)

        total = await self.match_repository.count_all(
            sport=sport,
            skill_level=skill_level,
            status=status,
            current_players=current_players,
            startdate=startdate,
            enddate=enddate,
            start_hour=start_hour,
            end_hour=end_hour,
            location=location,
        )

        return {
            "matches": matches,
            "total": total,
        }

    @staticmethod
    def _is_user_joined(match, current_user_id: str) -> bool:
        return any(player.user_id == current_user_id for player in match.players)
