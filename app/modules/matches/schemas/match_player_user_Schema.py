from pydantic import BaseModel, ConfigDict

from app.common.enums.skill_level import SkillLevel
from app.common.enums.sport_type import SportType


class MatchPlayerUserSchema(BaseModel):
    id: str
    username: str

    favorite_sport: SportType | None
    skill_level: SkillLevel | None

    model_config = ConfigDict(
        from_attributes=True,
    )
