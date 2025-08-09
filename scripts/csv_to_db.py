"""
Script to load CSV data into SQLite database
Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering
"""

import pandas as pd
import sys
import os

# Add the parent directory to the path to import api modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import SessionLocal, create_tables, Book
from api import schemas
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_csv_to_database(csv_file_path: str = "data/books.csv"):
    """Load books from CSV file into database"""
    
    # Create tables if they don't exist
    create_tables()
    
    # Read CSV file
    try:
        df = pd.read_csv(csv_file_path)
        logger.info(f"Successfully read CSV with {len(df)} records")
    except FileNotFoundError:
        logger.error(f"CSV file not found: {csv_file_path}")
        return False
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        return False
    
    # Clean and validate data
    df = df.fillna("")  # Fill NaN values with empty strings
    
    # Convert price to float, handling empty strings
    def safe_float_conversion(value):
        if pd.isna(value) or value == "" or value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    df['price'] = df['price'].apply(safe_float_conversion)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Book).delete()
        db.commit()
        logger.info("Cleared existing books from database")
        
        # Insert new data using bulk insert for better performance
        books_data = []
        for _, row in df.iterrows():
            book_data = {
                'title': row.get('title', ''),
                'price': row.get('price', 0.0),
                'rating': row.get('rating', ''),
                'availability': row.get('availability', ''),
                'category': row.get('category', ''),
                'image_url': row.get('image_url', ''),
                'link': row.get('link', '')
            }
            books_data.append(book_data)
        
        # Bulk insert all books at once - much faster than individual inserts
        db.bulk_insert_mappings(Book, books_data)
        books_created = len(books_data)
        
        db.commit()
        logger.info(f"Successfully loaded {books_created} books into database")
        
        # Verify data
        total_books = db.query(Book).count()
        logger.info(f"Total books in database: {total_books}")
        
        # Show some statistics
        categories = db.query(Book.category).distinct().count()
        avg_price = db.query(Book).filter(Book.price > 0).with_entities(
            db.func.avg(Book.price)
        ).scalar()
        
        logger.info(f"Categories: {categories}")
        logger.info(f"Average price: {avg_price:.2f}" if avg_price else "Average price: N/A")
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading data into database: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def rescrape_and_load():
    """Re-scrape data and load into database"""
    logger.info("Starting fresh scraping...")
    
    # Run the scraper
    import subprocess
    try:
        result = subprocess.run([
            sys.executable, "scripts/scrape_books.py"
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        if result.returncode == 0:
            logger.info("Scraping completed successfully")
            logger.info(result.stdout)
        else:
            logger.error("Scraping failed")
            logger.error(result.stderr)
            return False
    except Exception as e:
        logger.error(f"Error running scraper: {e}")
        return False
    
    # Load the new data
    return load_csv_to_database()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Load CSV data into database")
    parser.add_argument("--csv", default="data/books.csv", help="Path to CSV file")
    parser.add_argument("--rescrape", action="store_true", help="Re-scrape data before loading")
    
    args = parser.parse_args()
    
    if args.rescrape:
        success = rescrape_and_load()
    else:
        success = load_csv_to_database(args.csv)
    
    if success:
        logger.info("✅ Data loading completed successfully!")
    else:
        logger.error("❌ Data loading failed!")
        sys.exit(1)