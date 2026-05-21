from abc import ABC, abstractmethod

from app.modules.matches.infrastructure.database.models.match_player_model import (
    MatchPlayerModel,
)


class MatchPlayerRepository(ABC):
    @abstractmethod
    async def create(
        self,
        match_player: MatchPlayerModel,
    ) -> MatchPlayerModel: ...

    @abstractmethod
    async def delete(
        self,
        match_player: MatchPlayerModel,
    ) -> None: ...

    @abstractmethod
    async def get_by_match_and_user(
        match_id: str, user_id: str
    ) -> MatchPlayerModel | None: ...
