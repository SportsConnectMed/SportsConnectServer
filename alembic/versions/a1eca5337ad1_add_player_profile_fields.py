"""add player profile fields

Revision ID: a1eca5337ad1
Revises: df37d23eea10
Create Date: 2026-05-18 12:41:23.161518

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1eca5337ad1"
down_revision: Union[str, Sequence[str], None] = "df37d23eea10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sport_type_enum = sa.Enum(
        "FOOTBALL",
        "FUTSAL",
        "BASKETBALL",
        "VOLLEYBALL",
        "TENNIS",
        "PADEL",
        name="sporttype",
    )

    skill_level_enum = sa.Enum(
        "BEGINNER",
        "INTERMEDIATE",
        "ADVANCED",
        name="skilllevel",
    )

    sport_type_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    skill_level_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "users",
        sa.Column(
            "favorite_sport",
            sport_type_enum,
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "skill_level",
            skill_level_enum,
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "position",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "bio",
            sa.String(length=500),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "users",
        "bio",
    )

    op.drop_column(
        "users",
        "position",
    )

    op.drop_column(
        "users",
        "skill_level",
    )

    op.drop_column(
        "users",
        "favorite_sport",
    )

    sport_type_enum = sa.Enum(
        "FOOTBALL",
        "FUTSAL",
        "BASKETBALL",
        "VOLLEYBALL",
        "TENNIS",
        "PADEL",
        name="sporttype",
    )

    skill_level_enum = sa.Enum(
        "BEGINNER",
        "INTERMEDIATE",
        "ADVANCED",
        name="skilllevel",
    )

    sport_type_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )

    skill_level_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )
