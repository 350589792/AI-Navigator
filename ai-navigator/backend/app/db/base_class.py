"""SQLAlchemy declarative base class."""
from sqlalchemy.orm import declarative_base

# Create SQLAlchemy base class for declarative models
Base = declarative_base()

__all__ = ["Base"]
