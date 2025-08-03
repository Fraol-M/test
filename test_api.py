#!/usr/bin/env python3
"""
Test script for the Geocoding API
This script demonstrates how to use the FastAPI endpoints
"""

import httpx
import json

# API base URL (adjust if running on different port)
BASE_URL = "http://localhost:8000"

def test_search_places():
    """Test searching for places"""
    print("🔍 Testing place search...")
    
    # Test GET request
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/search", params={"query": "Berlin", "limit": 2})
        print(f"GET /search status: {response.status_code}")
        if response.status_code == 200:
            places = response.json()
            for place in places:
                print(f"  → {place['name']} ({place['country']}) at {place['coordinates']}")
    
    # Test POST request
    with httpx.Client() as client:
        data = {"query": "Paris", "limit": 2, "lang": "en"}
        response = client.post(f"{BASE_URL}/search", json=data)
        print(f"POST /search status: {response.status_code}")
        if response.status_code == 200:
            places = response.json()
            for place in places:
                print(f"  → {place['name']} ({place['country']}) at {place['coordinates']}")

def test_location_search():
    """Test location-based search"""
    print("\n📍 Testing location-based search...")
    
    # Test GET request
    with httpx.Client() as client:
        params = {
            "query": "Berlin",
            "lat": 52.3879,
            "lon": 13.0582
        }
        response = client.get(f"{BASE_URL}/search/location", params=params)
        print(f"GET /search/location status: {response.status_code}")
        if response.status_code == 200:
            places = response.json()
            if places:
                place = places[0]
                print(f"  → Closest match: {place['name']} ({place['country']})")
    
    # Test POST request
    with httpx.Client() as client:
        data = {
            "query": "Paris",
            "lat": 48.8566,
            "lon": 2.3522
        }
        response = client.post(f"{BASE_URL}/search/location", json=data)
        print(f"POST /search/location status: {response.status_code}")
        if response.status_code == 200:
            places = response.json()
            if places:
                place = places[0]
                print(f"  → Closest match: {place['name']} ({place['country']})")

def test_reverse_geocoding():
    """Test reverse geocoding"""
    print("\n🔄 Testing reverse geocoding...")
    
    # Test GET request
    with httpx.Client() as client:
        params = {"lat": 52.519854, "lon": 13.438596}
        response = client.get(f"{BASE_URL}/reverse", params=params)
        print(f"GET /reverse status: {response.status_code}")
        if response.status_code == 200:
            place_info = response.json()
            print(f"  → You are in: {place_info.get('name', 'Unknown')}, {place_info.get('country', 'Unknown')}")
    
    # Test POST request
    with httpx.Client() as client:
        data = {"lat": 48.8566, "lon": 2.3522}
        response = client.post(f"{BASE_URL}/reverse", json=data)
        print(f"POST /reverse status: {response.status_code}")
        if response.status_code == 200:
            place_info = response.json()
            print(f"  → You are in: {place_info.get('name', 'Unknown')}, {place_info.get('country', 'Unknown')}")

def test_health_check():
    """Test health check endpoint"""
    print("\n🏥 Testing health check...")
    
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/health")
        print(f"GET /health status: {response.status_code}")
        if response.status_code == 200:
            health = response.json()
            print(f"  → Service status: {health['status']}")

def test_root_endpoint():
    """Test root endpoint"""
    print("\n🏠 Testing root endpoint...")
    
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/")
        print(f"GET / status: {response.status_code}")
        if response.status_code == 200:
            info = response.json()
            print(f"  → API: {info['message']} v{info['version']}")

if __name__ == "__main__":
    print("🚀 Starting Geocoding API tests...")
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("=" * 50)
    
    try:
        test_root_endpoint()
        test_health_check()
        test_search_places()
        test_location_search()
        test_reverse_geocoding()
        
        print("\n✅ All tests completed!")
        print("\n📚 API Documentation available at: http://localhost:8000/docs")
        print("🔧 Interactive API docs at: http://localhost:8000/redoc")
        
    except httpx.ConnectError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the FastAPI server is running with: python src/main.py")
    except Exception as e:
        print(f"❌ Error during testing: {e}") 