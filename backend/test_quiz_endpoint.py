#!/usr/bin/env python3
"""
Test the quiz endpoint directly
"""

from database import SessionLocal, QuizAttempt, User
import requests
import json

def test_quiz_endpoint():
    """Test getting a quiz by ID"""
    db = SessionLocal()
    try:
        # Get an incomplete quiz
        incomplete_quiz = db.query(QuizAttempt).filter(
            QuizAttempt.status == 'incomplete'
        ).first()
        
        if not incomplete_quiz:
            print("❌ No incomplete quiz found")
            return
        
        print(f"✅ Found incomplete quiz ID: {incomplete_quiz.id}")
        print(f"   Topic: {incomplete_quiz.topic}")
        print(f"   Questions data: {incomplete_quiz.questions_data[:100]}...")
        
        # Test if questions_data is valid JSON
        if incomplete_quiz.questions_data:
            try:
                questions = json.loads(incomplete_quiz.questions_data)
                print(f"✅ Valid JSON with {len(questions)} questions")
                print(f"   First question: {questions[0]['question']}")
            except Exception as e:
                print(f"❌ Invalid JSON: {e}")
        else:
            print("❌ No questions_data")
        
        # Get user for auth test
        user = db.query(User).filter(User.id == incomplete_quiz.user_id).first()
        print(f"✅ Quiz belongs to user: {user.username}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_quiz_endpoint()