from abc import ABC, abstractmethod

from app.modules.matches.infrastructure.database.models.match_model import (
    MatchModel,
)


class MatchRepository(ABC):
    @abstractmethod
    async def create(
        self,
        match: MatchModel,
    ) -> MatchModel: ...

    @abstractmethod
    async def get_by_id(
        self,
        match_id: str,
    ) -> MatchModel | None: ...

    @abstractmethod
    async def get_all(self) -> list[MatchModel]: ...
