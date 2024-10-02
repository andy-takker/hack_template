import uuid

from sqlalchemy import ForeignKey, Index, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from hack_template.adapters.database.base import (
    Base,
    IdentifableMixin,
    TimestampedMixin,
)


class UserTable(IdentifableMixin, Base, TimestampedMixin):
    __tablename__ = "users"
    __table_args__ = (
        Index(
            None,
            "email",
            postgresql_where=text("email IS NOT NULL"),
            unique=True,
        ),
        Index(
            None,
            "telegram_id",
            postgresql_where=text("telegram_id IS NOT NULL"),
            unique=True,
        ),
    )
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str | None] = mapped_column(String(128), nullable=True)
    telegram_id: Mapped[int | None] = mapped_column(Integer, nullable=True)


class MessageTable(IdentifableMixin, Base):
    __tablename__ = "messages"
    to_user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    text: Mapped[str] = mapped_column(String(2047), nullable=False)
