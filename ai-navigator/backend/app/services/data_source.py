from datetime import datetime, UTC
from sqlalchemy.orm import Session
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
    async def initialize_preset_data(db: Session):
        """Initialize preset categories and data sources"""
        for category_data in PRESET_CATEGORIES:
            category = Category(
                name=category_data["name"],
                description=category_data["description"]
            )
            db.add(category)
            db.flush()  # Get category ID

            # Add preset sources for this category
            for source_data in PRESET_SOURCES[category_data["name"]]:
                source = DataSource(
                    name=source_data["name"],
                    url=source_data["url"],
                    category_id=category.id,
                    is_preset=True,
                    crawl_frequency=60  # Default to hourly
                )
                db.add(source)

        db.commit()

    @staticmethod
    async def create_data_source(db: Session, data_source: DataSourceCreate):
        """Create a new custom data source"""
        db_data_source = DataSource(
            name=data_source.name,
            url=data_source.url,
            category_id=data_source.category_id,
            is_preset=False,
            crawl_frequency=data_source.crawl_frequency
        )
        db.add(db_data_source)
        db.commit()
        db.refresh(db_data_source)
        return db_data_source

    @staticmethod
    async def get_data_sources_by_category(db: Session, category_id: int):
        """Get all data sources for a specific category"""
        return db.query(DataSource).filter(DataSource.category_id == category_id).all()

    @staticmethod
    async def update_last_crawled(db: Session, data_source_id: int):
        """Update the last_crawled timestamp for a data source"""
        data_source = db.query(DataSource).filter(DataSource.id == data_source_id).first()
        if data_source:
            data_source.last_crawled = datetime.now(UTC)
            db.commit()
            return True
        return False
