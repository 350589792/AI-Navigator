from sqlalchemy import Column, Integer, DateTime
from datetime import datetime, UTC

from app.db.base_class import Base

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
