"""add user role

Revision ID: df37d23eea10
Revises: 3b8c8356daaf
Create Date: 2026-05-17 14:22:42.640345

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "df37d23eea10"
down_revision: Union[str, Sequence[str], None] = "3b8c8356daaf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_role_enum = sa.Enum(
        "USER",
        "ADMIN",
        name="userrole",
    )

    user_role_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role_enum,
            nullable=False,
            server_default="USER",
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "users",
        "role",
    )

    user_role_enum = sa.Enum(
        "USER",
        "ADMIN",
        name="userrole",
    )

    user_role_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )
