from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.matches.infrastructure.database.models.match_model import (
        MatchModel,
    )
    from app.modules.users.infrastructure.database.models.user_model import (
        UserModel,
    )


class MatchPlayerModel(Base):
    __tablename__ = "match_players"

    __table_args__ = (
        UniqueConstraint(
            "match_id",
            "user_id",
            name="uq_match_player",
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    match_id: Mapped[str] = mapped_column(
        ForeignKey("matches.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    match: Mapped["MatchModel"] = relationship(
        back_populates="players",
    )

    user: Mapped["UserModel"] = relationship(
        back_populates="joined_matches",
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )
