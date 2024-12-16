from typing import AsyncGenerator
import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base
from app.models.models import Category

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True
)

# Create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

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

        for category in categories:
            session.add(category)

        await session.commit()
        logger.info("Initial data created successfully")
    except Exception as e:
        logger.error(f"Error creating initial data: {e}")
        await session.rollback()
        raise

async def init_db() -> None:
    """Initialize the database."""
    try:
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")

        # Create initial data
        async with async_session() as session:
            await create_initial_data(session)

    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
