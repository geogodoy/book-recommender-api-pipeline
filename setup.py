"""
Setup script for Book Recommender API
Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering
"""

import subprocess
import sys
import os


def install_requirements():
    """Install all required dependencies"""
    print("📦 Installing required dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def setup_database():
    """Setup database and load initial data"""
    print("🗃️  Setting up database...")
    try:
        # Import after dependencies are installed
        from scripts.csv_to_db import load_csv_to_database
        success = load_csv_to_database()
        if success:
            print("✅ Database setup completed!")
        else:
            print("❌ Database setup failed!")
        return success
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def run_scraper():
    """Run the web scraper to get fresh data"""
    print("🕷️  Running web scraper...")
    try:
        subprocess.check_call([sys.executable, "scripts/scrape_books.py"])
        print("✅ Scraping completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Scraping failed: {e}")
        return False


def main():
    """Main setup process"""
    print("🚀 Setting up Book Recommender API...")
    print("=" * 50)
    
    # Step 1: Install dependencies
    if not install_requirements():
        sys.exit(1)
    
    # Step 2: Check if we have data, if not scrape it
    csv_path = "data/books.csv"
    if not os.path.exists(csv_path):
        print("📄 No existing data found, running scraper...")
        if not run_scraper():
            sys.exit(1)
    else:
        print("📄 Existing data found, skipping scraper...")
    
    # Step 3: Setup database
    if not setup_database():
        sys.exit(1)
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\n🎯 Next steps:")
    print("1. Run the API: python main.py")
    print("2. View API docs: http://localhost:8000/docs")
    print("3. Test endpoints: http://localhost:8000/api/v1/health")


if __name__ == "__main__":
    main()