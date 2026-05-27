from datetime import date

from sqlalchemy import Date, cast, extract, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.matches.domain.repositories.match_repository import (
    MatchRepository,
)
from app.modules.matches.infrastructure.database.models.match_model import (
    MatchModel,
)
from app.modules.matches.infrastructure.database.models.match_player_model import (
    MatchPlayerModel,
)


class SQLAlchemyMatchRepository(MatchRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        match: MatchModel,
    ) -> MatchModel:
        self.db.add(match)

        await self.db.flush()

        return match

    async def save(self, match: MatchModel) -> MatchModel:
        self.db.add(match)

        await self.db.flush()

        await self.db.refresh(match)

        return match

    async def get_all(
        self,
        sport=None,
        skill_level=None,
        status=None,
        current_players=None,
        startdate: date | None = None,
        enddate: date | None = None,
        start_hour: int | None = None,
        end_hour: int | None = None,
        location: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ):

        statement = (
            self._build_filtered_query(
                sport=sport,
                skill_level=skill_level,
                status=status,
                current_players=current_players,
                startdate=startdate,
                enddate=enddate,
                start_hour=start_hour,
                end_hour=end_hour,
                location=location,
            )
            .options(
                selectinload(MatchModel.players).selectinload(MatchPlayerModel.user)
            )
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.db.execute(statement)

        return list(result.scalars().all())

    async def count_all(
        self,
        sport=None,
        skill_level=None,
        status=None,
        current_players=None,
        startdate: date | None = None,
        enddate: date | None = None,
        start_hour: int | None = None,
        end_hour: int | None = None,
        location: str | None = None,
    ) -> int:

        statement = select(func.count()).select_from(MatchModel)

        statement = self._apply_filters(
            statement,
            sport=sport,
            skill_level=skill_level,
            status=status,
            current_players=current_players,
            startdate=startdate,
            enddate=enddate,
            start_hour=start_hour,
            end_hour=end_hour,
            location=location,
        )

        result = await self.db.execute(statement)

        return result.scalar_one()

    async def get_by_id(
        self,
        match_id: str,
    ) -> MatchModel | None:

        statement = (
            select(MatchModel)
            .where(MatchModel.id == match_id)
            .options(
                selectinload(MatchModel.players).selectinload(MatchPlayerModel.user)
            )
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def get_my_matches(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 10,
    ) -> list[MatchModel]:

        statement = (
            select(MatchModel)
            .where(
                or_(
                    MatchModel.creator_id == user_id,
                    MatchModel.players.any(user_id=user_id),
                )
            )
            .options(
                selectinload(MatchModel.players).selectinload(MatchPlayerModel.user)
            )
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.db.execute(statement)

        return list(result.scalars().all())

    async def count_my_matches(
        self,
        user_id: str,
    ) -> int:

        statement = (
            select(func.count())
            .select_from(MatchModel)
            .where(
                or_(
                    MatchModel.creator_id == user_id,
                    MatchModel.players.any(user_id=user_id),
                )
            )
        )

        result = await self.db.execute(statement)

        return result.scalar_one()

    def _build_filtered_query(
        self,
        sport=None,
        skill_level=None,
        status=None,
        current_players=None,
        startdate: date | None = None,
        enddate: date | None = None,
        start_hour: int | None = None,
        end_hour: int | None = None,
        location: str | None = None,
    ):
        statement = select(MatchModel)

        return self._apply_filters(
            statement,
            sport=sport,
            skill_level=skill_level,
            status=status,
            current_players=current_players,
            startdate=startdate,
            enddate=enddate,
            start_hour=start_hour,
            end_hour=end_hour,
            location=location,
        )

    def _apply_filters(
        self,
        statement,
        sport=None,
        skill_level=None,
        status=None,
        current_players=None,
        startdate: date | None = None,
        enddate: date | None = None,
        start_hour: int | None = None,
        end_hour: int | None = None,
        location: str | None = None,
    ):
        if sport:
            statement = statement.where(MatchModel.sport == sport)

        if skill_level:
            statement = statement.where(MatchModel.skill_level == skill_level)

        if status:
            statement = statement.where(MatchModel.status == status)

        if current_players is not None:
            statement = statement.where(MatchModel.current_players == current_players)

        scheduled_date = cast(MatchModel.scheduled_at, Date)

        if startdate is not None and enddate is not None:
            statement = statement.where(scheduled_date.between(startdate, enddate))
        elif startdate is not None:
            statement = statement.where(scheduled_date >= startdate)
        elif enddate is not None:
            statement = statement.where(scheduled_date <= enddate)

        scheduled_hour = extract("hour", MatchModel.scheduled_at)

        if start_hour is not None and end_hour is not None:
            statement = statement.where(scheduled_hour.between(start_hour, end_hour))
        elif start_hour is not None:
            statement = statement.where(scheduled_hour >= start_hour)
        elif end_hour is not None:
            statement = statement.where(scheduled_hour <= end_hour)

        if location:
            statement = statement.where(MatchModel.location.ilike(f"%{location}%"))

        return statement
