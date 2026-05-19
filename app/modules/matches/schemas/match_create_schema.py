from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.common.enums.skill_level import SkillLevel
from app.common.enums.sport_type import SportType


class MatchCreateSchema(BaseModel):
    title: Annotated[
        str,
        Field(min_length=3, max_length=100),
    ]

    description: Annotated[
        str | None,
        Field(max_length=500),
    ] = None

    sport: SportType

    skill_level: SkillLevel

    location: Annotated[
        str,
        Field(min_length=3, max_length=255),
    ]

    max_players: Annotated[
        int,
        Field(gt=1, le=100),
    ]

    scheduled_at: datetime

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )
