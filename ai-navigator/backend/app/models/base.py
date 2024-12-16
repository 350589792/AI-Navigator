from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime, UTC

# Create base class for SQLAlchemy declarative models
Base = declarative_base()


class TimestampMixin:
    """Mixin for adding created_at and updated_at timestamps to models."""
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False
    )


class BaseModel(Base):
    """Abstract base model with common fields."""
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
