from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums.skill_level import SkillLevel
from app.common.enums.sport_type import SportType
from app.core.database import Base
from app.modules.matches.domain.enums.match_status import MatchStatus

if TYPE_CHECKING:
    from app.modules.matches.infrastructure.database.models.match_player_model import (
        MatchPlayerModel,
    )
    from app.modules.users.infrastructure.database.models.user_model import (
        UserModel,
    )


class MatchModel(Base):
    __tablename__ = "matches"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    sport: Mapped[SportType] = mapped_column(
        Enum(
            SportType,
            name="sporttype",
            create_type=True,
        ),
        nullable=False,
    )

    skill_level: Mapped[SkillLevel] = mapped_column(
        Enum(
            SkillLevel,
            name="skilllevel",
            create_type=True,
        ),
        nullable=False,
    )

    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    max_players: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    current_players: Mapped[int] = mapped_column(
        Integer,
        default=1,  # The first player is the match creator always
        nullable=False,
    )

    status: Mapped[MatchStatus] = mapped_column(
        Enum(
            MatchStatus,
            name="matchstatus",
            create_type=True,
        ),
        default=MatchStatus.OPEN,
        nullable=False,
    )

    creator_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    creator: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="created_matches"
    )

    players: Mapped[list["MatchPlayerModel"]] = relationship(
        "MatchPlayerModel",
        back_populates="match",
        cascade="all, delete-orphan",
    )

    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )
