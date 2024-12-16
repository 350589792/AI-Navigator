import pytest
from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from app.models.models import User, Category, NotificationSetting
from app.services.data_source import DataSourceService


@pytest.mark.asyncio
async def test_user_category_preferences(db: Session):
    """Test user category preferences"""
    # Initialize preset categories
    await DataSourceService.initialize_preset_data(db)

    # Create test user
    user = User(
        email="test@example.com",
        hashed_password="hashed_password"
    )
    db.add(user)
    db.commit()

    # Get categories
    categories = db.query(Category).all()

    # Set user preferences
    user.preferred_categories = categories[:2]  # Select first two categories
    db.commit()

    # Verify preferences
    db_user = db.query(User).filter(User.email == "test@example.com").first()
    assert len(db_user.preferred_categories) == 2
    category_names = {cat.name for cat in db_user.preferred_categories}
    assert category_names == {categories[0].name, categories[1].name}


@pytest.mark.asyncio
async def test_notification_settings(db: Session):
    """Test notification settings"""
    # Create test user
    user = User(
        email="test@example.com",
        hashed_password="hashed_password"
    )
    db.add(user)
    db.commit()

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
    db.commit()
    db.refresh(notification_setting)

    # Verify settings
    settings = db.query(NotificationSetting).filter(
        NotificationSetting.user_id == user.id
    ).first()

    assert settings is not None
    assert settings.email_enabled is True
    assert settings.pdf_enabled is True
    assert settings.in_app_enabled is True
    # Compare timezone-aware datetimes
    time_diff = abs(settings.delivery_time.replace(tzinfo=UTC) - delivery_time)
    assert time_diff < timedelta(seconds=1)
