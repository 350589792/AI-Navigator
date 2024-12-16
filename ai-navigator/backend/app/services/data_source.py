from datetime import datetime, UTC
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Category, DataSource
from app.schemas.data_source import DataSourceCreate


PRESET_CATEGORIES = [
    {"name": "新闻", "description": "新闻资讯"},
    {"name": "科技", "description": "科技动态"},
    {"name": "财经", "description": "财经资讯"},
    {"name": "体育", "description": "体育新闻"}
]


PRESET_SOURCES = {
    "新闻": [{"name": "新浪新闻", "url": "https://news.sina.com.cn/"}],
    "科技": [{"name": "36氪", "url": "https://36kr.com/"}],
    "财经": [{"name": "东方财富", "url": "https://www.eastmoney.com/"}],
    "体育": [{"name": "腾讯体育", "url": "https://sports.qq.com/"}]
}


class DataSourceService:
    @staticmethod
    async def initialize_preset_data(db: AsyncSession):
        """Initialize preset categories and data sources"""
        # Create categories first
        categories = {}
        for category_data in PRESET_CATEGORIES:
            category = Category(
                name=category_data["name"],
                description=category_data["description"]
            )
            db.add(category)
            await db.flush()
            categories[category.name] = category

        # Then create data sources for each category
        for category_name, sources in PRESET_SOURCES.items():
            category = categories[category_name]
            for source_data in sources:
                source = DataSource(
                    name=source_data["name"],
                    url=source_data["url"],
                    category_id=category.id,
                    is_preset=True,
                    crawl_frequency=60  # Default to hourly
                )
                db.add(source)
                await db.flush()

    @staticmethod
    async def create_data_source(db: AsyncSession, data_source: DataSourceCreate):
        """Create a new custom data source"""
        db_data_source = DataSource(
            name=data_source.name,
            url=data_source.url,
            category_id=data_source.category_id,
            is_preset=False,
            crawl_frequency=data_source.crawl_frequency
        )
        db.add(db_data_source)
        await db.flush()  # Get the ID
        return db_data_source

    @staticmethod
    async def get_data_sources_by_category(db: AsyncSession, category_id: int):
        """Get all data sources for a specific category"""
        result = await db.execute(
            select(DataSource).filter(DataSource.category_id == category_id)
        )
        return result.scalars().all()

    @staticmethod
    async def update_last_crawled(db: AsyncSession, data_source_id: int):
        """Update the last_crawled timestamp for a data source"""
        result = await db.execute(
            select(DataSource).filter(DataSource.id == data_source_id)
        )
        data_source = result.scalar_one_or_none()
        if data_source:
            data_source.last_crawled = datetime.now(UTC)
            await db.flush()
            return True
        return False
