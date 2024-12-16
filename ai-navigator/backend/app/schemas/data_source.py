from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class DataSourceBase(BaseModel):
    """Base schema for data source."""
    name: str
    url: str
    category_id: int
    description: Optional[str] = None
    crawl_frequency: int = 30  # Default to 30 minutes


class DataSourceCreate(DataSourceBase):
    """Schema for creating a data source."""
    pass


class DataSource(DataSourceBase):
    """Schema for a data source with database fields."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryBase(BaseModel):
    """Base schema for category."""
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Schema for creating a category."""
    pass


class Category(CategoryBase):
    """Schema for a category with database fields."""
    id: int
    data_sources: List[DataSource] = []

    model_config = ConfigDict(from_attributes=True)
