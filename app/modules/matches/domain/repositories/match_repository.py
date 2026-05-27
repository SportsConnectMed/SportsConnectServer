from abc import ABC, abstractmethod
from datetime import date

from app.common.enums.skill_level import SkillLevel
from app.common.enums.sport_type import SportType
from app.modules.matches.domain.enums.match_status import MatchStatus
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
    async def save(self, match: MatchModel) -> MatchModel: ...

    @abstractmethod
    async def get_by_id(
        self,
        match_id: str,
    ) -> MatchModel | None: ...

    @abstractmethod
    async def get_all(
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
    ) -> list[MatchModel]: ...

    @abstractmethod
    async def count_all(
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
    ) -> int: ...

    @abstractmethod
    async def get_my_matches(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 10,
    ) -> list[MatchModel]: ...

    @abstractmethod
    async def count_my_matches(
        self,
        user_id: str,
    ) -> int: ...
