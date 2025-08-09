"""
Database configuration and models for the Book Recommender API
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/books.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Book(Base):
    """Book model for database"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    price = Column(Float, index=True, nullable=True)  # Add index for price queries
    rating = Column(String, index=True, nullable=True)  # Add index for rating queries
    availability = Column(String, nullable=True)
    category = Column(String, index=True, nullable=True)
    image_url = Column(Text, nullable=True)
    link = Column(Text, nullable=True)


def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()