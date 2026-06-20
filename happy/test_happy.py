"""
HAPPY V0.1 Test Script
Test all core functionality of HAPPY backend
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def print_response(title: str, response: dict):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}")
    print(json.dumps(response, indent=2))

def test_health():
    """Test health check"""
    print("\n🏥 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response.json())

def test_open_app(app: str):
    """Test opening an app"""
    print(f"\n🚀 Testing: Open {app}")
    response = requests.post(
        f"{BASE_URL}/app",
        json={"command": f"open {app}"}
    )
    print_response(f"Open {app}", response.json())

def test_remember(statement: str):
    """Test remembering something"""
    print(f"\n💾 Testing: Remember command")
    response = requests.post(
        f"{BASE_URL}/app",
        json={"command": f"remember {statement}"}
    )
    print_response("Remember", response.json())

def test_recall(query: str):
    """Test recalling something"""
    print(f"\n🧠 Testing: Recall command")
    response = requests.post(
        f"{BASE_URL}/app",
        json={"command": f"what is my {query}"}
    )
    print_response("Recall", response.json())

def test_create_folder(folder: str):
    """Test creating a folder"""
    print(f"\n📁 Testing: Create folder")
    response = requests.post(
        f"{BASE_URL}/app",
        json={"command": f"create folder {folder}"}
    )
    print_response("Create Folder", response.json())

def test_get_memories():
    """Test getting all memories"""
    print(f"\n📖 Testing: Get all memories")
    response = requests.get(f"{BASE_URL}/memory")
    print_response("All Memories", response.json())

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🎉 HAPPY V0.1 - Test Suite")
    print("="*60)
    
    try:
        # Test 1: Health
        test_health()
        time.sleep(0.5)
        
        # Test 2: Open Notepad
        test_open_app("notepad")
        time.sleep(0.5)
        
        # Test 3: Remember
        test_remember("my favorite color is blue")
        time.sleep(0.5)
        
        # Test 4: Recall
        test_recall("favorite color")
        time.sleep(0.5)
        
        # Test 5: Create Folder
        test_create_folder("HAPPY_DEMO")
        time.sleep(0.5)
        
        # Test 6: Get all memories
        test_get_memories()
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to HAPPY backend")
        print("   Make sure the server is running:")
        print("   cd backend && python -m uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
