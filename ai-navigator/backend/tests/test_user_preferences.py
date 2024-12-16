import pytest
from datetime import datetime, timedelta, UTC
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.models import User, Category, NotificationSetting, UserCategoryAssociation
from app.services.data_source import DataSourceService

@pytest.mark.asyncio
async def test_user_category_preferences(db: AsyncSession):
    """Test user category preferences"""
    # Clean up existing data
    async with db.begin():
        await db.execute(delete(UserCategoryAssociation))
        await db.execute(delete(NotificationSetting))
        await db.execute(delete(User))
        await db.execute(delete(Category))

    # Initialize preset categories
    async with db.begin():
        await DataSourceService.initialize_preset_data(db)

    # Create test user and associations
    async with db.begin():
        # Create user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password"
        )
        db.add(user)
        await db.flush()

        # Get categories
        stmt = select(Category)
        result = await db.execute(stmt)
        categories = result.scalars().all()

        # Create associations directly
        for category in categories[:2]:  # Select first two categories
            association = UserCategoryAssociation(
                user_id=user.id,
                category_id=category.id
            )
            db.add(association)

    # Verify preferences
    async with db.begin():
        stmt = (
            select(User)
            .options(selectinload(User.preferred_categories))
            .filter(User.email == "test@example.com")
        )
        result = await db.execute(stmt)
        db_user = result.unique().scalar_one()

        assert len(db_user.preferred_categories) == 2
        category_names = {cat.name for cat in db_user.preferred_categories}
        assert len(category_names) == 2
        assert all(cat.name in category_names for cat in categories[:2])

@pytest.mark.asyncio
async def test_notification_settings(db: AsyncSession):
    """Test notification settings"""
    # Clean up existing data
    async with db.begin():
        await db.execute(delete(NotificationSetting))
        await db.execute(delete(User))

    # Create test user and settings
    async with db.begin():
        # Create user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password"
        )
        db.add(user)
        await db.flush()

        # Create notification settings with timezone-aware datetime
        delivery_time = datetime.now(UTC) + timedelta(hours=1)
        notification_setting = NotificationSetting(
            user_id=user.id,
            delivery_time=delivery_time,
            email_enabled=True,
            pdf_enabled=True,
            in_app_enabled=True
        )
        db.add(notification_setting)

    # Verify settings
    async with db.begin():
        stmt = (
            select(NotificationSetting)
            .filter(NotificationSetting.user_id == user.id)
        )
        result = await db.execute(stmt)
        settings = result.scalar_one()

        assert settings is not None
        assert settings.email_enabled is True
        assert settings.pdf_enabled is True
        assert settings.in_app_enabled is True
        # Compare timezone-aware datetimes
        time_diff = abs(settings.delivery_time.replace(tzinfo=UTC) - delivery_time)
        assert time_diff < timedelta(seconds=1)
