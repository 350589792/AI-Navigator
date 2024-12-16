from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


# Create SQLAlchemy base class for declarative models
Base = declarative_base()


# Create engine and session factory
def get_engine(database_url: str):
    """Create SQLAlchemy engine with the given database URL."""
    return create_engine(database_url)


def get_session_factory(engine):
    """Create SQLAlchemy session factory bound to the given engine."""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
