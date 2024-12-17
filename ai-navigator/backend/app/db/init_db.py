import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Category


logger = logging.getLogger(__name__)


async def create_initial_data(session: AsyncSession) -> None:
    """Create initial data in the database."""
    try:
        # Create default categories
        categories = [
            Category(name="News", description="General news articles"),
            Category(name="Technology", description="Technology news and updates"),
            Category(name="Finance", description="Financial news and market updates"),
            Category(name="Sports", description="Sports news and updates")
        ]

        # Add all categories at once
        session.add_all(categories)
        await session.flush()
        logger.info("Initial data created successfully")
    except Exception as e:
        logger.error(f"Error creating initial data: {e}")
        raise


async def init_db(session: AsyncSession) -> None:
    """Initialize the database with initial data."""
    try:
        # Create initial data
        await create_initial_data(session)
        await session.commit()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        await session.rollback()
        raise
