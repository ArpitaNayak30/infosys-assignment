#!/usr/bin/env python3
"""
Create a test incomplete quiz for testing resume functionality
"""

from database import SessionLocal, QuizAttempt, User
import json
from datetime import datetime, timezone

def create_test_quiz():
    """Create a test incomplete quiz"""
    db = SessionLocal()
    try:
        # Get the first user (assuming you have at least one user)
        user = db.query(User).first()
        if not user:
            print("❌ No users found. Please register a user first.")
            return
        
        # Sample questions
        test_questions = [
            {
                "question": "What is the capital of France?",
                "options": ["A) London", "B) Berlin", "C) Paris", "D) Madrid"]
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["A) Venus", "B) Mars", "C) Jupiter", "D) Saturn"]
            },
            {
                "question": "What is 2 + 2?",
                "options": ["A) 3", "B) 4", "C) 5", "D) 6"]
            }
        ]
        
        # Create incomplete quiz attempt
        quiz_attempt = QuizAttempt(
            user_id=user.id,
            topic="Test Quiz",
            total_questions=3,
            questions_data=json.dumps(test_questions),
            status="incomplete"
        )
        
        db.add(quiz_attempt)
        db.commit()
        db.refresh(quiz_attempt)
        
        print(f"✅ Created test incomplete quiz with ID: {quiz_attempt.id}")
        print(f"   User: {user.username}")
        print(f"   Topic: {quiz_attempt.topic}")
        print(f"   Status: {quiz_attempt.status}")
        
    except Exception as e:
        print(f"❌ Failed to create test quiz: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_quiz()