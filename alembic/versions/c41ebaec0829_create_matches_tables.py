"""create matches tables

Revision ID: c41ebaec0829
Revises: a1eca5337ad1
Create Date: 2026-05-19 13:35:38.000705
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c41ebaec0829"
down_revision: Union[str, Sequence[str], None] = "a1eca5337ad1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "matches",
        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "sport",
            postgresql.ENUM(
                "FOOTBALL",
                "FUTSAL",
                "BASKETBALL",
                "VOLLEYBALL",
                "TENNIS",
                "PADEL",
                name="sporttype",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "skill_level",
            postgresql.ENUM(
                "BEGINNER",
                "INTERMEDIATE",
                "ADVANCED",
                name="skilllevel",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "location",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "max_players",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "current_players",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "OPEN",
                "FULL",
                "FINISHED",
                "CANCELLED",
                name="matchstatus",
            ),
            nullable=False,
        ),
        sa.Column(
            "creator_id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "scheduled_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["creator_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "match_players",
        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "match_id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "joined_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["match_id"],
            ["matches.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "match_id",
            "user_id",
            name="uq_match_player",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("match_players")
    op.drop_table("matches")
