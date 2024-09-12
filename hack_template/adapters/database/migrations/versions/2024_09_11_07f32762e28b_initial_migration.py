from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "07f32762e28b"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("password", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=128), nullable=True),
        sa.Column("telegram_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__users")),
        sa.UniqueConstraint("username", name=op.f("uq__users__username")),
    )
    op.create_index(
        op.f("ix__users__email"),
        "users",
        ["email"],
        unique=True,
        postgresql_where=sa.text("email IS NOT NULL"),
    )
    op.create_index(
        op.f("ix__users__telegram_id"),
        "users",
        ["telegram_id"],
        unique=True,
        postgresql_where=sa.text("telegram_id IS NOT NULL"),
    )
    op.create_table(
        "messages",
        sa.Column("to_user_id", sa.UUID(), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("text", sa.String(length=2047), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["to_user_id"], ["users.id"], name=op.f("fk__messages__to_user_id__users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__messages")),
    )


def downgrade() -> None:
    op.drop_table("messages")
    op.drop_index(
        op.f("ix__users__telegram_id"),
        table_name="users",
        postgresql_where=sa.text("telegram_id IS NOT NULL"),
    )
    op.drop_index(
        op.f("ix__users__email"),
        table_name="users",
        postgresql_where=sa.text("email IS NOT NULL"),
    )
    op.drop_table("users")
