#!/usr/bin/env python3
"""
Test script for the Question Generator API
This script demonstrates how to use the /api/generate-questions endpoint
"""

import requests
import json
import time

# API Configuration
BASE_URL = "http://127.0.0.1:8000"
GENERATE_QUESTIONS_ENDPOINT = f"{BASE_URL}/api/generate-questions"

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

def test_generate_questions(topic, number_questions):
    """Test the generate questions endpoint"""
    print(f"\n🧪 Testing question generation for topic: '{topic}' with {number_questions} questions")
    
    payload = {
        "topic": topic,
        "number_questions": number_questions
    }
    
    try:
        print("📤 Sending request...")
        start_time = time.time()
        
        response = requests.post(
            GENERATE_QUESTIONS_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
        
        print(f"⏱️  Response time: {response_time} seconds")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Request successful!")
            print(f"📝 Generated {len(data['questions'])} questions")
            
            # Display the questions
            for i, question in enumerate(data['questions'], 1):
                print(f"\n--- Question {i} ---")
                print(f"Q: {question['question']}")
                for j, option in enumerate(question['options'], 1):
                    print(f"  {j}. {option}")
            
            return True
        else:
            print(f"❌ Request failed with status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        return False

def test_validation_errors():
    """Test API validation with invalid inputs"""
    print("\n🔍 Testing API validation...")
    
    test_cases = [
        {"topic": "", "number_questions": 5, "expected": "empty topic"},
        {"topic": "Math", "number_questions": 0, "expected": "invalid number (too low)"},
        {"topic": "Science", "number_questions": 25, "expected": "invalid number (too high)"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest case {i}: {test_case['expected']}")
        payload = {
            "topic": test_case["topic"],
            "number_questions": test_case["number_questions"]
        }
        
        response = requests.post(
            GENERATE_QUESTIONS_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        if response.status_code == 400:
            print(f"✅ Validation working correctly - Status: {response.status_code}")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            print(f"Response: {response.text}")

def main():
    """Main test function"""
    print("🚀 Question Generator API Test Script")
    print("=" * 50)
    
    # Test API health
    if not test_api_health():
        print("\n❌ API is not available. Please start the server with:")
        print("   cd backend")
        print("   uvicorn main:app --reload")
        return
    
    # Test successful cases
    test_cases = [
        {"topic": "Chemistry", "number_questions": 3},
        {"topic": "World History", "number_questions": 2},
        {"topic": "Python Programming", "number_questions": 4},
        {"topic": "Mathematics", "number_questions": 1},
    ]
    
    print("\n📚 Testing successful question generation...")
    for test_case in test_cases:
        success = test_generate_questions(test_case["topic"], test_case["number_questions"])
        if not success:
            break
        time.sleep(1)  # Small delay between requests
    
    # Test validation
    test_validation_errors()
    
    print("\n🎉 Test script completed!")
    print("\n💡 Usage examples:")
    print("   curl -X POST http://127.0.0.1:8000/api/generate-questions \\")
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"topic": "Physics", "number_questions": 5}\'')

if __name__ == "__main__":
    main()