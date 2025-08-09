"""
Script to run the FastAPI application
Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering
"""

import uvicorn
import sys
import os

def main():
    """Run the FastAPI application"""
    print("🚀 Starting Book Recommender API...")
    print("📚 API Documentation will be available at: http://localhost:8000/docs")
    print("🔍 Interactive API docs: http://localhost:8000/redoc")
    print("❤️  Health check: http://localhost:8000/api/v1/health")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,  # Auto-reload on code changes
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 API shutdown complete!")
    except Exception as e:
        print(f"❌ Error starting API: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()