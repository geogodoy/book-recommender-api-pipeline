"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel
from typing import List, Optional


class BookBase(BaseModel):
    """Base book schema"""
    title: str
    price: Optional[float] = None
    rating: Optional[str] = None
    availability: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    link: Optional[str] = None


class BookCreate(BookBase):
    """Schema for creating a book"""
    pass


class Book(BookBase):
    """Complete book schema with ID"""
    id: int

    class Config:
        from_attributes = True


class BookSearchParams(BaseModel):
    """Search parameters for books"""
    title: Optional[str] = None
    category: Optional[str] = None


class PriceRangeParams(BaseModel):
    """Price range parameters"""
    min_price: Optional[float] = None
    max_price: Optional[float] = None


class StatsOverview(BaseModel):
    """Statistics overview schema"""
    total_books: int
    average_price: Optional[float]
    rating_distribution: dict
    categories_count: int


class CategoryStats(BaseModel):
    """Category statistics schema"""
    category: str
    book_count: int
    average_price: Optional[float]
    min_price: Optional[float]
    max_price: Optional[float]


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    database_connected: bool
    total_books: int