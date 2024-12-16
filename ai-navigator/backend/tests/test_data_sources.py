import pytest
from sqlalchemy.orm import Session
from app.models.models import Category, DataSource
from app.services.data_source import DataSourceService, PRESET_CATEGORIES

@pytest.mark.asyncio
async def test_initialize_preset_data(db: Session):
    """Test initialization of preset categories and data sources"""
    await DataSourceService.initialize_preset_data(db)

    # Verify categories
    categories = db.query(Category).all()
    assert len(categories) == len(PRESET_CATEGORIES)
    category_names = {cat.name for cat in categories}
    expected_names = {cat["name"] for cat in PRESET_CATEGORIES}
    assert category_names == expected_names

    # Verify each category has exactly one preset source
    for category in categories:
        sources = await DataSourceService.get_data_sources_by_category(db, category.id)
        assert len(sources) == 1
        assert sources[0].is_preset == True

@pytest.mark.asyncio
async def test_create_custom_data_source(db: Session):
    """Test creating a custom data source"""
    # First create a category
    category = Category(name="Test Category", description="Test Description")
    db.add(category)
    db.commit()

    # Create custom data source
    from app.schemas.data_source import DataSourceCreate
    data_source_data = DataSourceCreate(
        name="Test Source",
        url="https://test.com",
        category_id=category.id,
        crawl_frequency=30
    )

    data_source = await DataSourceService.create_data_source(db, data_source_data)
    assert data_source.name == "Test Source"
    assert data_source.url == "https://test.com"
    assert data_source.category_id == category.id
    assert data_source.is_preset == False
    assert data_source.crawl_frequency == 30

@pytest.mark.asyncio
async def test_update_last_crawled(db: Session):
    """Test updating last_crawled timestamp"""
    # Create a test data source
    category = Category(name="Test Category", description="Test Description")
    db.add(category)
    db.commit()

    data_source = DataSource(
        name="Test Source",
        url="https://test.com",
        category_id=category.id,
        is_preset=False,
        crawl_frequency=30
    )
    db.add(data_source)
    db.commit()

    # Update last_crawled
    success = await DataSourceService.update_last_crawled(db, data_source.id)
    assert success == True

    # Verify timestamp was updated
    updated_source = db.query(DataSource).filter(DataSource.id == data_source.id).first()
    assert updated_source.last_crawled is not None
