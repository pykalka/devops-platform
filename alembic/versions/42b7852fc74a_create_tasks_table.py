"""create tasks table

Revision ID: 42b7852fc74a
Revises: 
Create Date: 2026-09-11 00:40:59.952783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42b7852fc74a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create tasks table."""
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_tasks_id"),
        "tasks",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop tasks table."""
    op.drop_index(
        op.f("ix_tasks_id"),
        table_name="tasks",
    )

    op.drop_table("tasks")
