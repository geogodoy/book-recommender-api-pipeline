"""
CRUD operations for books
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from . import schemas
from .database import Book


def get_book(db: Session, book_id: int) -> Optional[Book]:
    """Get a book by ID"""
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    """Get all books with pagination"""
    return db.query(Book).offset(skip).limit(limit).all()


def search_books(
    db: Session, 
    title: Optional[str] = None, 
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Book]:
    """Search books by title and/or category"""
    query = db.query(Book)
    
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    
    if category:
        query = query.filter(Book.category.ilike(f"%{category}%"))
    
    return query.offset(skip).limit(limit).all()


def get_books_by_price_range(
    db: Session, 
    min_price: Optional[float] = None, 
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Book]:
    """Get books within a price range"""
    query = db.query(Book)
    
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Book.price <= max_price)
    
    return query.offset(skip).limit(limit).all()


def get_top_rated_books(db: Session, limit: int = 20) -> List[Book]:
    """Get top rated books (sorted by rating) - Optimized version"""
    # Use SQL CASE WHEN for rating sorting directly in database
    from sqlalchemy import case
    
    rating_order = case(
        (Book.rating == 'Five', 5),
        (Book.rating == 'Four', 4),
        (Book.rating == 'Three', 3),
        (Book.rating == 'Two', 2),
        (Book.rating == 'One', 1),
        else_=0
    )
    
    # Let the database do the sorting and limiting
    books = db.query(Book).order_by(rating_order.desc()).limit(limit).all()
    return books


def get_categories(db: Session) -> List[str]:
    """Get all unique categories"""
    categories = db.query(Book.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]


def get_stats_overview(db: Session) -> dict:
    """Get overview statistics"""
    total_books = db.query(Book).count()
    avg_price = db.query(func.avg(Book.price)).scalar()
    
    # Rating distribution
    rating_counts = db.query(Book.rating, func.count(Book.rating)).group_by(Book.rating).all()
    rating_distribution = {rating: count for rating, count in rating_counts if rating}
    
    categories_count = db.query(Book.category).distinct().count()
    
    return {
        "total_books": total_books,
        "average_price": round(avg_price, 2) if avg_price else None,
        "rating_distribution": rating_distribution,
        "categories_count": categories_count
    }


def get_category_stats(db: Session) -> List[dict]:
    """Get statistics by category"""
    categories = get_categories(db)
    stats = []
    
    for category in categories:
        books_in_category = db.query(Book).filter(Book.category == category)
        
        book_count = books_in_category.count()
        avg_price = books_in_category.with_entities(func.avg(Book.price)).scalar()
        min_price = books_in_category.with_entities(func.min(Book.price)).scalar()
        max_price = books_in_category.with_entities(func.max(Book.price)).scalar()
        
        stats.append({
            "category": category,
            "book_count": book_count,
            "average_price": round(avg_price, 2) if avg_price else None,
            "min_price": min_price,
            "max_price": max_price
        })
    
    return stats


def create_book(db: Session, book: schemas.BookCreate) -> Book:
    """Create a new book"""
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def bulk_create_books(db: Session, books: List[schemas.BookCreate]) -> int:
    """Bulk create books"""
    db_books = [Book(**book.dict()) for book in books]
    db.add_all(db_books)
    db.commit()
    return len(db_books)