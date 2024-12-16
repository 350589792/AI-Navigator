import asyncio
import os
import pytest
import pytest_asyncio
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    async_scoped_session,
)
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import database_exists, create_database, drop_database
from asyncio import current_task

from app.db.base_class import Base
from app.db.init_db import init_db
# Import all models to ensure they are registered with SQLAlchemy
from app.models.models import (  # noqa: F401
    User, Category, DataSource, NotificationSetting, UserCategoryAssociation
)
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set testing environment
os.environ["TESTING"] = "1"

# Test database URL matching CI environment
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
SYNC_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("+asyncpg", "")


@pytest.fixture(scope="session")
def event_loop_policy():
    """Create and set a custom event loop policy for the test session."""
    return asyncio.get_event_loop_policy()


@pytest.fixture(scope="session")
def event_loop(event_loop_policy):
    """Create an instance of the default event loop for the test session."""
    loop = event_loop_policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    """Create a new engine for the test session."""
    engine = None
    sync_engine = None

    try:
        # Create sync engine for database operations
        sync_engine = create_engine(SYNC_DATABASE_URL)

        # Create database if it doesn't exist
        if not database_exists(sync_engine.url):
            create_database(sync_engine.url)

        # Create async engine with minimal configuration
        engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL,
            echo=True,
            poolclass=NullPool,
            future=True
        )

        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield engine

    except Exception as e:
        logger.error(f"Error setting up database: {e}")
        raise
    finally:
        # Cleanup
        if engine:
            await engine.dispose()
        if sync_engine:
            sync_engine.dispose()
            if database_exists(sync_engine.url):
                drop_database(sync_engine.url)


@pytest_asyncio.fixture
async def db(db_engine) -> AsyncSession:
    """Get a database session for testing."""
    # Create session factory
    session_factory = async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )

    # Create scoped session factory bound to the current task
    async_session = async_scoped_session(
        session_factory,
        scopefunc=current_task
    )

    try:
        # Create a new session
        session = async_session()

        # Clean existing data within transaction
        async with session.begin():
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(text(f"TRUNCATE TABLE {table.name} CASCADE"))
            await init_db(session)

        yield session

    except Exception as e:
        logger.error(f"Error in database fixture: {e}")
        raise
    finally:
        await session.close()
        await async_session.remove()
