from pydantic import BaseModel

from app.modules.matches.schemas.match_response_schema import MatchResponseSchema


class MatchListResponseSchema(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    matches: list[MatchResponseSchema]
