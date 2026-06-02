from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.common.enums.skill_level import SkillLevel
from app.common.enums.sport_type import SportType
from app.modules.matches.domain.enums.match_status import MatchStatus
from app.modules.matches.schemas.match_player_response_schema import MatchPlayerResponseSchema


class MatchResponseSchema(BaseModel):
    id: str
    title: str
    description: str | None

    sport: SportType
    skill_level: SkillLevel

    location: str

    max_players: int
    current_players: int

    status: MatchStatus

    creator_id: str

    players: list[MatchPlayerResponseSchema]
    is_joined: bool = False

    scheduled_at: datetime
    created_at: datetime

    latitude: float | None
    longitude: float | None

    model_config = ConfigDict(
        from_attributes=True,
    )

    @classmethod
    def from_match(cls, match: Any, current_user_id: str) -> "MatchResponseSchema":
        response = cls.model_validate(match)
        is_joined = getattr(match, "is_joined", None)

        if is_joined is None:
            is_joined = cls._is_user_joined(match, current_user_id)

        response.is_joined = is_joined

        return response

    @staticmethod
    def _is_user_joined(match: Any, current_user_id: str) -> bool:
        return any(player.user_id == current_user_id for player in match.players)
