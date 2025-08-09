"""
Setup script para ambiente de produção (Render)
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
    """Main production setup process"""
    logger.info("🚀 Setting up Book Recommender API for Production...")
    logger.info("=" * 60)
    
    # Step 1: Install dependencies
    if not install_requirements():
        logger.error("❌ Failed to install dependencies.")
        sys.exit(1)
    
    # Step 2: Setup data directory
    setup_data_directory()
    
    # Step 3: Run scraper to get fresh data
    if not run_scraper():
        logger.error("❌ Failed to scrape data.")
        sys.exit(1)
    
    # Step 4: Setup database
    if not setup_database():
        logger.error("❌ Failed to setup database.")
        sys.exit(1)
    
    logger.info("=" * 60)
    logger.info("✅ Production setup completed successfully!")
    logger.info("🚀 API will be available shortly...")

if __name__ == "__main__":
    main()