import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.db.base import Base
from app.core.config import settings
from app.models.models import *  # Import all models to ensure they're registered

# Test database URL matching CI environment
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/test_db"

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create test database and tables."""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists(engine.url):
        create_database(engine.url)

    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield engine

    # Drop database after all tests
    drop_database(engine.url)

@pytest.fixture(scope="function")
def db_session(setup_test_db):
    """Create a new database session for a test."""
    connection = setup_test_db.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def db(db_session):
    """Alias for db_session to match test function signatures."""
    return db_session
