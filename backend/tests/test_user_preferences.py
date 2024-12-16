import pytest
from datetime import datetime, timedelta
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

    # Create notification settings
    delivery_time = datetime.utcnow() + timedelta(hours=1)
    notification_setting = NotificationSetting(
        user_id=user.id,
        delivery_time=delivery_time,
        email_enabled=True,
        pdf_enabled=True,
        in_app_enabled=True
    )
    db.add(notification_setting)
    db.commit()

    # Verify settings
    db_user = db.query(User).filter(User.email == "test@example.com").first()
    assert len(db_user.notification_settings) == 1
    settings = db_user.notification_settings[0]
    assert settings.email_enabled == True
    assert settings.pdf_enabled == True
    assert settings.in_app_enabled == True
    assert abs(settings.delivery_time - delivery_time) < timedelta(seconds=1)
