"""
Smart Production Setup - Evita duplicação no deploy
Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering
"""

import subprocess
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_requirements():
    """Install all required dependencies"""
    logger.info("📦 Installing production dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt",
            "--no-cache-dir"
        ])
        logger.info("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error installing dependencies: {e}")
        return False

def setup_data_directory():
    """Create data directory if it doesn't exist"""
    logger.info("📁 Setting up data directory...")
    os.makedirs("data", exist_ok=True)
    logger.info("✅ Data directory ready!")

def check_existing_data():
    """Check if we already have valid data"""
    csv_path = "data/books.csv"
    db_path = "data/books.db"
    
    # Check if CSV exists and has content
    csv_exists = os.path.exists(csv_path) and os.path.getsize(csv_path) > 1000  # At least 1KB
    
    # Check if database exists and has content
    if os.path.exists(db_path):
        try:
            # Quick check if database has data
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM books LIMIT 1")
            count = cursor.fetchone()[0]
            conn.close()
            db_has_data = count > 0
        except:
            db_has_data = False
    else:
        db_has_data = False
    
    logger.info(f"📊 Data status: CSV exists: {csv_exists}, DB has data: {db_has_data}")
    return csv_exists and db_has_data

def run_scraper():
    """Run the web scraper to get fresh data"""
    logger.info("🕷️  Running web scraper for fresh data...")
    
    try:
        subprocess.check_call([sys.executable, "scripts/scrape_books.py"])
        logger.info("✅ Scraping completed!")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Scraping failed: {e}")
        return False

def setup_database():
    """Setup database and load initial data"""
    logger.info("🗃️  Setting up production database...")
    try:
        # Import after dependencies are installed
        from scripts.csv_to_db import load_csv_to_database
        success = load_csv_to_database()
        if success:
            logger.info("✅ Database setup completed!")
        else:
            logger.error("❌ Database setup failed!")
        return success
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False

def main():
    """Smart production setup process"""
    logger.info("🚀 Setting up Book Recommender API for Production (Smart Mode)...")
    logger.info("=" * 60)
    
    # Step 1: Install dependencies
    if not install_requirements():
        logger.error("❌ Failed to install dependencies.")
        sys.exit(1)
    
    # Step 2: Setup data directory
    setup_data_directory()
    
    # Step 3: Smart data management
    if check_existing_data():
        logger.info("📊 Existing valid data found, skipping scraping...")
        logger.info("🔄 This prevents unnecessary load on the source website")
        logger.info("⚡ Deploy will be faster!")
    else:
        logger.info("📄 No valid data found, running scraper...")
        if not run_scraper():
            logger.error("❌ Failed to scrape data.")
            sys.exit(1)
    
    # Step 4: Setup database (only if needed)
    if not os.path.exists("data/books.db") or os.path.getsize("data/books.db") < 1000:
        if not setup_database():
            logger.error("❌ Failed to setup database.")
            sys.exit(1)
    else:
        logger.info("🗃️  Existing database found, skipping reload...")
    
    logger.info("=" * 60)
    logger.info("✅ Smart production setup completed successfully!")
    logger.info("🚀 API will be available shortly...")
    logger.info("💡 This deploy was optimized to avoid unnecessary scraping!")

if __name__ == "__main__":
    main()