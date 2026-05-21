from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.common.enums.skill_level import SkillLevel
from app.common.enums.sport_type import SportType
from app.modules.matches.domain.enums.match_status import MatchStatus


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

    scheduled_at: datetime
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
