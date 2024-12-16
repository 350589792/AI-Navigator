import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.db.base import Base
# These imports are needed to register models with SQLAlchemy
from app.models.models import (  # noqa: F401
    User, Category, DataSource, NotificationSetting
)
from app.core.config import settings


# Test database URL matching CI environment
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Create test database and tables."""
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

    # Create database if it doesn't exist
    sync_engine = engine.sync_engine
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop database after all tests
    await engine.dispose()
    if database_exists(sync_engine.url):
        drop_database(sync_engine.url)


@pytest_asyncio.fixture(scope="function")
async def db_session(setup_test_db):
    """Create a new database session for a test."""
    async with setup_test_db.connect() as connection:
        await connection.begin()

        async_session = sessionmaker(
            connection,
            class_=AsyncSession,
            expire_on_commit=False
        )

        async with async_session() as session:
            yield session
            await session.rollback()


@pytest.fixture(scope="function")
async def db(db_session):
    """Alias for db_session to match test function signatures."""
    return db_session
