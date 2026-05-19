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
