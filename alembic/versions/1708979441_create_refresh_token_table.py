"""create refresh_token table

Revision ID: 79a1a1a86059
Revises: 094ab13e6cd0
Create Date: 2024-02-26 20:30:41.735542+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "79a1a1a86059"
down_revision: Union[str, None] = "094ab13e6cd0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME: str = "refresh_token"


def upgrade() -> None:
    op.create_table(
        TABLE_NAME,
        sa.Column("uuid", sa.UUID, primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("app_user.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token", sa.String, nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table(TABLE_NAME)
