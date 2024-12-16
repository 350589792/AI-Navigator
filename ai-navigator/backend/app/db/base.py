"""Database base module for importing all models."""
# Import Base and models
from app.db.base_class import Base
from app.models.models import (  # noqa: F401
    User,
    Category,
    DataSource,
    NotificationSetting
)

# Make sure all models are loaded and registered with SQLAlchemy
__all__ = [
    "Base",
    "User",
    "Category",
    "DataSource",
    "NotificationSetting"
]

# Verify tables after all models are imported
tables = Base.metadata.tables.keys()
required_tables = {'users', 'categories', 'data_sources', 'notification_settings'}
if not required_tables.issubset(tables):
    missing = required_tables - set(tables)
    raise ImportError(f"Missing required tables: {missing}")
