"""
Script de testes para validar API em produção
Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering
"""

import requests
import sys
import json
import time
from typing import Dict, Any

def test_endpoint(base_url: str, endpoint: str, expected_status: int = 200, params: Dict = None) -> Dict[str, Any]:
    """Test a single endpoint"""
    url = f"{base_url}{endpoint}"
    
    try:
        print(f"🧪 Testing: {endpoint}")
        start_time = time.time()
        
        response = requests.get(url, params=params, timeout=30)
        response_time = time.time() - start_time
        
        result = {
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response_time": round(response_time, 3),
            "success": response.status_code == expected_status,
            "content_type": response.headers.get("content-type", ""),
            "data_size": len(response.content)
        }
        
        if response.status_code == expected_status:
            print(f"   ✅ Status: {response.status_code} | Time: {response_time:.3f}s")
            try:
                data = response.json()
                if isinstance(data, list):
                    result["data_count"] = len(data)
                elif isinstance(data, dict) and "total_books" in data:
                    result["total_books"] = data["total_books"]
            except:
                pass
        else:
            print(f"   ❌ Status: {response.status_code} (expected {expected_status})")
            result["error"] = response.text[:200]
        
        return result
        
    except requests.exceptions.Timeout:
        print(f"   ⏰ Timeout after 30 seconds")
        return {"endpoint": endpoint, "success": False, "error": "Timeout"}
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error: {str(e)}")
        return {"endpoint": endpoint, "success": False, "error": str(e)}

def run_production_tests(base_url: str):
    """Run comprehensive tests on production API"""
    
    print("🚀 Testing Book Recommender API in Production")
    print(f"🌐 Base URL: {base_url}")
    print("=" * 60)
    
    # Define test cases
    test_cases = [
        # Basic endpoints
        {"endpoint": "/", "description": "Root endpoint"},
        {"endpoint": "/api/v1/health", "description": "Health check"},
        {"endpoint": "/api/v1/status", "description": "Quick status"},
        {"endpoint": "/api/v1/data-status", "description": "Data status"},
        
        # Core functionality
        {"endpoint": "/api/v1/books", "params": {"limit": 5}, "description": "List books (limit 5)"},
        {"endpoint": "/api/v1/books/1", "description": "Get specific book"},
        {"endpoint": "/api/v1/categories", "description": "List categories"},
        
        # Search functionality
        {"endpoint": "/api/v1/books/search", "params": {"title": "the"}, "description": "Search by title"},
        {"endpoint": "/api/v1/books/search", "params": {"category": "fiction"}, "description": "Search by category"},
        
        # Stats endpoints
        {"endpoint": "/api/v1/stats/overview", "description": "Stats overview"},
        {"endpoint": "/api/v1/stats/categories", "description": "Category stats"},
        {"endpoint": "/api/v1/books/top-rated", "params": {"limit": 5}, "description": "Top rated books"},
        {"endpoint": "/api/v1/books/price-range", "params": {"min_price": 10, "max_price": 30}, "description": "Price range filter"},
        
        # Documentation
        {"endpoint": "/docs", "description": "Swagger documentation"},
        {"endpoint": "/redoc", "description": "ReDoc documentation"}
    ]
    
    results = []
    successful_tests = 0
    
    for test_case in test_cases:
        endpoint = test_case["endpoint"]
        params = test_case.get("params", None)
        description = test_case["description"]
        
        print(f"\n📋 {description}")
        result = test_endpoint(base_url, endpoint, params=params)
        results.append(result)
        
        if result.get("success", False):
            successful_tests += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Successful tests: {successful_tests}/{len(test_cases)}")
    print(f"❌ Failed tests: {len(test_cases) - successful_tests}/{len(test_cases)}")
    
    # Detailed results
    print("\n📋 DETAILED RESULTS:")
    for result in results:
        status = "✅" if result.get("success", False) else "❌"
        endpoint = result["endpoint"]
        status_code = result.get("status_code", "N/A")
        response_time = result.get("response_time", "N/A")
        
        print(f"{status} {endpoint:30} | Status: {status_code:3} | Time: {response_time}s")
        
        if "data_count" in result:
            print(f"   📊 Data count: {result['data_count']}")
        elif "total_books" in result:
            print(f"   📚 Total books: {result['total_books']}")
        
        if not result.get("success", False) and "error" in result:
            print(f"   ⚠️  Error: {result['error']}")
    
    # Performance analysis
    response_times = [r.get("response_time", 0) for r in results if "response_time" in r]
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        print(f"\n⚡ PERFORMANCE:")
        print(f"   Average response time: {avg_time:.3f}s")
        print(f"   Slowest response: {max_time:.3f}s")
    
    return successful_tests == len(test_cases)

def main():
    """Main test function"""
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        base_url = input("🌐 Enter the production URL (e.g., https://your-app.onrender.com): ").rstrip('/')
    
    if not base_url:
        print("❌ No URL provided!")
        sys.exit(1)
    
    # Validate URL format
    if not base_url.startswith(('http://', 'https://')):
        print("❌ URL must start with http:// or https://")
        sys.exit(1)
    
    print(f"\n🎯 Starting tests for: {base_url}")
    time.sleep(2)  # Give server time if it was just deployed
    
    success = run_production_tests(base_url)
    
    if success:
        print("\n🎉 All tests passed! API is working correctly in production.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()