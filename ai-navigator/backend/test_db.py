from app.core.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database

print(f'Testing connection to: {settings.DATABASE_URL}')
sync_url = settings.DATABASE_URL.replace('+asyncpg', '')
engine = create_engine(sync_url)

if not database_exists(engine.url):
    print('Creating database...')
    create_database(engine.url)
    print('Database created successfully')
else:
    print('Database exists')

print('Testing connection...')
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('Connection successful!')
    print(result.fetchone())
