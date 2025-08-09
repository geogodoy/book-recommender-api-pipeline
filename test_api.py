"""
Test script for Book Recommender API endpoints
Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering
"""

import requests
import json
import time


BASE_URL = "http://localhost:8000"


def test_endpoint(endpoint, expected_status=200, params=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=params)
        status = "✅" if response.status_code == expected_status else "❌"
        print(f"{status} {endpoint} - Status: {response.status_code}")
        
        if response.status_code == expected_status:
            data = response.json()
            if isinstance(data, list):
                print(f"    📋 Returned {len(data)} items")
            elif isinstance(data, dict):
                if 'total_books' in data:
                    print(f"    📊 Total books: {data['total_books']}")
                elif 'message' in data:
                    print(f"    💬 Message: {data['message']}")
        else:
            print(f"    ❌ Error: {response.text}")
        
        return response.status_code == expected_status
    
    except requests.exceptions.ConnectionError:
        print(f"❌ {endpoint} - Connection refused (is the API running?)")
        return False
    except Exception as e:
        print(f"❌ {endpoint} - Error: {e}")
        return False


def main():
    """Run all API tests"""
    print("🧪 Testing Book Recommender API...")
    print("=" * 50)
    
    # Check if API is running
    print("🔍 Checking if API is running...")
    if not test_endpoint("/"):
        print("❌ API is not running! Please start it with: python run_api.py")
        return
    
    print("\n📋 Testing Core Endpoints:")
    
    # Core endpoints
    test_endpoint("/api/v1/health")
    test_endpoint("/api/v1/books?limit=5")
    test_endpoint("/api/v1/books/1")
    test_endpoint("/api/v1/categories")
    
    print("\n🔍 Testing Search Endpoints:")
    test_endpoint("/api/v1/books/search", params={"title": "python"})
    test_endpoint("/api/v1/books/search", params={"category": "travel"})
    
    print("\n📊 Testing Stats Endpoints:")
    test_endpoint("/api/v1/stats/overview")
    test_endpoint("/api/v1/stats/categories")
    test_endpoint("/api/v1/books/top-rated")
    test_endpoint("/api/v1/books/price-range", params={"min_price": 10, "max_price": 50})
    
    print("\n🚫 Testing Error Cases:")
    test_endpoint("/api/v1/books/99999", expected_status=404)
    test_endpoint("/api/v1/books/search", expected_status=400)  # No search params
    
    print("\n=" * 50)
    print("✅ API testing completed!")
    print("\n🎯 Quick API usage examples:")
    print(f"📚 Get all books: curl {BASE_URL}/api/v1/books")
    print(f"🔍 Search books: curl '{BASE_URL}/api/v1/books/search?title=python'")
    print(f"📊 Get stats: curl {BASE_URL}/api/v1/stats/overview")


if __name__ == "__main__":
    main()