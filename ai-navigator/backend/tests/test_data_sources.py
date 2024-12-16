import pytest
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Category, DataSource
from app.services.data_source import DataSourceService, PRESET_CATEGORIES, PRESET_SOURCES


@pytest.mark.asyncio(scope="function")
async def test_initialize_preset_data(db: AsyncSession):
    """Test initialization of preset categories and data sources"""
    async with db.begin():
        # Clean up any existing data
        await db.execute(delete(DataSource))
        await db.execute(delete(Category))
        await db.flush()

        # Initialize preset data
        await DataSourceService.initialize_preset_data(db)
        await db.flush()

        # Verify categories
        result = await db.execute(select(Category))
        categories = result.scalars().all()
        assert len(categories) == len(PRESET_CATEGORIES)
        category_names = {cat.name for cat in categories}
        expected_names = {cat["name"] for cat in PRESET_CATEGORIES}
        assert category_names == expected_names

        # Verify each category has its preset sources
        total_sources = 0
        for category in categories:
            result = await db.execute(
                select(DataSource).filter(DataSource.category_id == category.id)
            )
            sources = result.scalars().all()
            expected_sources = len(PRESET_SOURCES[category.name])
            assert len(sources) == expected_sources, f"Category {category.name} should have {expected_sources} sources but has {len(sources)}"
            total_sources += len(sources)
            for source in sources:
                assert source.is_preset is True
                assert source.category_id == category.id

        # Verify total number of sources
        total_expected_sources = sum(len(sources) for sources in PRESET_SOURCES.values())
        assert total_sources == total_expected_sources


@pytest.mark.asyncio(scope="function")
async def test_create_custom_data_source(db: AsyncSession):
    """Test creating a custom data source"""
    async with db.begin():
        # Clean up any existing data
        await db.execute(delete(DataSource))
        await db.execute(delete(Category))
        await db.flush()

        # Create a category
        category = Category(name="Test Category", description="Test Description")
        db.add(category)
        await db.flush()

        # Create custom data source
        from app.schemas.data_source import DataSourceCreate
        data_source_data = DataSourceCreate(
            name="Test Source",
            url="https://test.com",
            category_id=category.id,
            crawl_frequency=30
        )

        data_source = await DataSourceService.create_data_source(
            db, data_source_data
        )
        await db.flush()

        # Verify the data source was created correctly
        result = await db.execute(
            select(DataSource).filter(DataSource.id == data_source.id)
        )
        created_source = result.scalar_one()
        assert created_source.name == "Test Source"
        assert created_source.url == "https://test.com"
        assert created_source.category_id == category.id
        assert created_source.is_preset is False
        assert created_source.crawl_frequency == 30


@pytest.mark.asyncio(scope="function")
async def test_update_last_crawled(db: AsyncSession):
    """Test updating last_crawled timestamp"""
    async with db.begin():
        # Clean up any existing data
        await db.execute(delete(DataSource))
        await db.execute(delete(Category))
        await db.flush()

        # Create a test data source
        category = Category(name="Test Category", description="Test Description")
        db.add(category)
        await db.flush()

        data_source = DataSource(
            name="Test Source",
            url="https://test.com",
            category_id=category.id,
            is_preset=False,
            crawl_frequency=30
        )
        db.add(data_source)
        await db.flush()

        # Update last_crawled
        success = await DataSourceService.update_last_crawled(db, data_source.id)
        assert success is True

        # Verify timestamp was updated
        result = await db.execute(
            select(DataSource).filter(DataSource.id == data_source.id)
        )
        updated_source = result.scalar_one()
        assert updated_source.last_crawled is not None
