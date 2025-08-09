"""
Manual data update script
Execute este script apenas quando quiser atualizar os dados
Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering
"""

import logging
import sys
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Atualizar dados manualmente"""
    logger.info("🔄 Manual data update initiated...")
    logger.info("This will scrape fresh data and update the database")
    
    # Confirm action
    confirm = input("Are you sure you want to update data? This will replace existing data. (y/N): ")
    if confirm.lower() != 'y':
        logger.info("❌ Update cancelled")
        return
    
    # Run scraper
    import subprocess
    try:
        logger.info("🕷️  Running web scraper...")
        subprocess.check_call([sys.executable, "scripts/scrape_books.py"])
        logger.info("✅ Scraping completed!")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Scraping failed: {e}")
        sys.exit(1)
    
    # Update database
    try:
        from scripts.csv_to_db import load_csv_to_database
        success = load_csv_to_database()
        if success:
            logger.info("✅ Database updated successfully!")
        else:
            logger.error("❌ Database update failed!")
            sys.exit(1)
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        sys.exit(1)
    
    logger.info("🎉 Data update completed successfully!")

if __name__ == "__main__":
    main()