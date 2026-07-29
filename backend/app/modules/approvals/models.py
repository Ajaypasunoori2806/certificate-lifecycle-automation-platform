from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    certificate_id: Mapped[int] = mapped_column(
        ForeignKey("certificates.id"),
        nullable=False,
    )

    approver_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    approver_email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    approval_status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
    )

    comments: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    certificate = relationship(
        "Certificate",
        back_populates="approvals",
    )