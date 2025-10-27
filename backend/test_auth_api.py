#!/usr/bin/env python3
"""
Test script for the Question Generator API with Authentication
This script demonstrates how to use the authentication endpoints
"""

import requests
import json
import time

# API Configuration
BASE_URL = "http://127.0.0.1:8000"
AUTH_BASE = f"{BASE_URL}/api/auth"
QUESTIONS_ENDPOINT = f"{BASE_URL}/api/generate-questions"

# Test user data
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123"
}

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ API is running successfully")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ API health check failed with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False

def test_user_registration():
    """Test user registration"""
    print(f"\n🧪 Testing user registration...")
    
    response = requests.post(
        f"{AUTH_BASE}/register",
        headers={"Content-Type": "application/json"},
        json=TEST_USER
    )
    
    print(f"📊 Status code: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print("✅ User registration successful!")
        print(f"👤 User ID: {data['id']}")
        print(f"👤 Username: {data['username']}")
        print(f"📧 Email: {data['email']}")
        return True
    elif response.status_code == 400:
        print("⚠️  User already exists (this is expected on subsequent runs)")
        return True
    else:
        print(f"❌ Registration failed: {response.text}")
        return False

def test_user_login():
    """Test user login and return token"""
    print(f"\n🔐 Testing user login...")
    
    login_data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    }
    
    response = requests.post(
        f"{AUTH_BASE}/login",
        headers={"Content-Type": "application/json"},
        json=login_data
    )
    
    print(f"📊 Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Login successful!")
        print(f"🎫 Token type: {data['token_type']}")
        print(f"👤 User: {data['user']['username']}")
        return data['access_token']
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_protected_endpoint(token):
    """Test accessing protected endpoint with token"""
    print(f"\n🔒 Testing protected endpoint (user profile)...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{AUTH_BASE}/profile", headers=headers)
    
    print(f"📊 Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Protected endpoint access successful!")
        print(f"👤 Profile: {data['username']} ({data['email']})")
        return True
    else:
        print(f"❌ Protected endpoint access failed: {response.text}")
        return False

def test_question_generation_with_auth(token):
    """Test question generation with authentication"""
    print(f"\n📚 Testing question generation with authentication...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "topic": "Python Programming",
        "number_questions": 2
    }
    
    response = requests.post(QUESTIONS_ENDPOINT, headers=headers, json=payload)
    
    print(f"📊 Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Authenticated question generation successful!")
        print(f"📝 Generated {len(data['questions'])} questions")
        
        for i, question in enumerate(data['questions'], 1):
            print(f"\n--- Question {i} ---")
            print(f"Q: {question['question']}")
            for j, option in enumerate(question['options'], 1):
                print(f"  {j}. {option}")
        return True
    else:
        print(f"❌ Question generation failed: {response.text}")
        return False

def test_unauthorized_access():
    """Test accessing protected endpoint without token"""
    print(f"\n🚫 Testing unauthorized access...")
    
    payload = {
        "topic": "Math",
        "number_questions": 1
    }
    
    response = requests.post(
        QUESTIONS_ENDPOINT,
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    print(f"📊 Status code: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ Unauthorized access properly blocked!")
        return True
    else:
        print(f"⚠️  Unexpected response: {response.text}")
        return False

def test_logout(token):
    """Test user logout"""
    print(f"\n👋 Testing user logout...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{AUTH_BASE}/logout", headers=headers)
    
    print(f"📊 Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Logout successful!")
        print(f"💬 Message: {data['message']}")
        return True
    else:
        print(f"❌ Logout failed: {response.text}")
        return False

def main():
    """Main test function"""
    print("🚀 Question Generator API Authentication Test Script")
    print("=" * 60)
    
    # Test API health
    if not test_api_health():
        print("\n❌ API is not available. Please start the server with:")
        print("   cd backend")
        print("   python setup_database.py  # First time only")
        print("   uvicorn main:app --reload")
        return
    
    # Test authentication flow
    print("\n🔐 Testing Authentication Flow...")
    
    # 1. Register user
    if not test_user_registration():
        return
    
    # 2. Login user
    token = test_user_login()
    if not token:
        return
    
    # 3. Test protected endpoint
    if not test_protected_endpoint(token):
        return
    
    # 4. Test question generation with auth
    if not test_question_generation_with_auth(token):
        return
    
    # 5. Test unauthorized access
    test_unauthorized_access()
    
    # 6. Test logout
    test_logout(token)
    
    print("\n🎉 All authentication tests completed!")
    
    print("\n💡 API Endpoints Summary:")
    print("   POST /api/auth/register    - Register new user")
    print("   POST /api/auth/login       - Login user")
    print("   POST /api/auth/logout      - Logout user")
    print("   GET  /api/auth/profile     - Get user profile")
    print("   POST /api/generate-questions - Generate questions (requires auth)")

if __name__ == "__main__":
    main()