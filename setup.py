"""
Setup script for Book Recommender API
Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering
"""

import subprocess
import sys
import os
import platform
import venv


def create_virtual_environment():
    """Create a Python virtual environment"""
    venv_path = "venv"
    
    print("🐍 Creating Python virtual environment...")
    
    # Check if virtual environment already exists and is valid
    if os.path.exists(venv_path):
        python_executable = get_venv_python_path(venv_path)
        if os.path.exists(python_executable):
            print("✅ Valid virtual environment already exists, using existing one...")
            return True, venv_path
        else:
            print("⚠️  Virtual environment directory exists but Python executable not found.")
            print("🔄 Removing corrupted virtual environment and recreating...")
            try:
                import shutil
                shutil.rmtree(venv_path)
            except Exception as e:
                print(f"❌ Error removing corrupted virtual environment: {e}")
                return False, None
    
    try:
        # Create virtual environment
        print("🔨 Creating new virtual environment...")
        venv.create(venv_path, with_pip=True)
        
        # Verify the Python executable was created
        python_executable = get_venv_python_path(venv_path)
        if os.path.exists(python_executable):
            print("✅ Virtual environment created successfully!")
            return True, venv_path
        else:
            print("❌ Virtual environment created but Python executable not found!")
            return False, None
            
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False, None


def get_venv_python_path(venv_path):
    """Get the Python executable path from virtual environment"""
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:
        return os.path.join(venv_path, "bin", "python")


def install_requirements(venv_path=None):
    """Install all required dependencies"""
    print("📦 Installing required dependencies...")
    
    # Determine which Python executable to use
    if venv_path:
        python_executable = get_venv_python_path(venv_path)
        
        # Double-check if the executable exists
        if not os.path.exists(python_executable):
            print(f"⚠️  Virtual environment Python not found at: {python_executable}")
            print("🔄 Falling back to system Python...")
            python_executable = sys.executable
        else:
            print(f"🔧 Using virtual environment Python: {python_executable}")
    else:
        python_executable = sys.executable
        print(f"🔧 Using system Python: {python_executable}")
    
    try:
        # Install requirements with explicit PyPI index URL
        cmd = [
            python_executable, "-m", "pip", "install", "-r", "requirements.txt",
            "--index-url", "https://pypi.org/simple/"
        ]
        print(f"🚀 Running command: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    except FileNotFoundError as e:
        print(f"❌ Python executable not found: {e}")
        print("💡 Try using system Python instead...")
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


def run_scraper(venv_path=None):
    """Run the web scraper to get fresh data"""
    print("🕷️  Running web scraper...")
    
    # Determine which Python executable to use
    if venv_path:
        python_executable = get_venv_python_path(venv_path)
        
        # Double-check if the executable exists
        if not os.path.exists(python_executable):
            print(f"⚠️  Virtual environment Python not found at: {python_executable}")
            print("🔄 Falling back to system Python...")
            python_executable = sys.executable
    else:
        python_executable = sys.executable
    
    try:
        subprocess.check_call([python_executable, "scripts/scrape_books.py"])
        print("✅ Scraping completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Scraping failed: {e}")
        return False
    except FileNotFoundError as e:
        print(f"❌ Python executable not found: {e}")
        return False


def main():
    """Main setup process"""
    print("🚀 Setting up Book Recommender API...")
    print("=" * 50)
    
    # Step 1: Create virtual environment
    success, venv_path = create_virtual_environment()
    if not success:
        print("⚠️  Virtual environment creation failed, continuing with system Python...")
        venv_path = None
    
    # Step 2: Install dependencies (in virtual environment if available, otherwise system)
    if not install_requirements(venv_path):
        print("❌ Failed to install dependencies. Please check your Python and pip installation.")
        sys.exit(1)
    
    # Step 3: Check if we have data, if not scrape it
    csv_path = "data/books.csv"
    if not os.path.exists(csv_path):
        print("📄 No existing data found, running scraper...")
        if not run_scraper(venv_path):
            sys.exit(1)
    else:
        print("📄 Existing data found, skipping scraper...")
    
    # Step 4: Setup database
    if not setup_database():
        sys.exit(1)
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\n🎯 Next steps:")
    venv_python = get_venv_python_path(venv_path)
    print(f"1. Activate virtual environment:")
    if platform.system() == "Windows":
        print(f"   .\\{venv_path}\\Scripts\\activate")
    else:
        print(f"   source {venv_path}/bin/activate")
    print(f"2. Run the API: {venv_python} main.py")
    print("3. View API docs: http://localhost:8000/docs")
    print("4. Test endpoints: http://localhost:8000/api/v1/health")


if __name__ == "__main__":
    main()