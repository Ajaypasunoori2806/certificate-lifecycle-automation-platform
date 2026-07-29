from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id"),
        nullable=False,
    )

    certificate_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    common_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    issuer: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    serial_number: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    certificate_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    environment: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    issued_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    expiry_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="ACTIVE",
    )

    renewal_reminder_days: Mapped[int] = mapped_column(
        Integer,
        default=30,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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

    # Relationship with Application
    application: Mapped["Application"] = relationship(
        "Application",
        back_populates="certificates",
    )

    # Relationship with Approval
    approvals: Mapped[list["Approval"]] = relationship(
        "Approval",
        back_populates="certificate",
        cascade="all, delete-orphan",
    )

    # Relationship with Notification
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="certificate",
        cascade="all, delete-orphan",
    )