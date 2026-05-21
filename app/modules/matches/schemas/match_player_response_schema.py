from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.modules.matches.schemas.match_player_user_Schema import MatchPlayerUserSchema


class MatchPlayerResponseSchema(BaseModel):
    id: str

    joined_at: datetime

    user: MatchPlayerUserSchema

    model_config = ConfigDict(
        from_attributes=True,
    )
