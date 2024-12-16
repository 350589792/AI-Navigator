from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    DateTime, Boolean, Table
)
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseModel, TimestampMixin


# Association table for user preferences
user_category_association = Table(
    'user_category_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


class Category(BaseModel, TimestampMixin):
    __tablename__ = "categories"

    name = Column(String, unique=True, index=True)
    description = Column(String)
    data_sources = relationship("DataSource", back_populates="category")
    users = relationship(
        "User",
        secondary=user_category_association,
        back_populates="preferred_categories"
    )


class DataSource(BaseModel, TimestampMixin):
    __tablename__ = "data_sources"

    name = Column(String, index=True)
    url = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_preset = Column(Boolean, default=False)
    crawl_frequency = Column(Integer)  # in minutes
    last_crawled = Column(DateTime(timezone=True), nullable=True)

    category = relationship("Category", back_populates="data_sources")


class User(BaseModel, TimestampMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    preferred_categories = relationship(
        "Category",
        secondary=user_category_association,
        back_populates="users"
    )
    notification_settings = relationship(
        "NotificationSetting",
        back_populates="user"
    )


class NotificationSetting(BaseModel, TimestampMixin):
    __tablename__ = "notification_settings"

    user_id = Column(Integer, ForeignKey("users.id"))
    delivery_time = Column(DateTime(timezone=True))
    email_enabled = Column(Boolean, default=True)
    pdf_enabled = Column(Boolean, default=True)
    in_app_enabled = Column(Boolean, default=True)

    user = relationship("User", back_populates="notification_settings")
