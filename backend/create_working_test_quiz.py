#!/usr/bin/env python3
"""
Create a working test quiz that can be resumed
"""

from database import SessionLocal, QuizAttempt, User
import json
from datetime import datetime, timezone

def create_working_quiz():
    """Create a working incomplete quiz"""
    db = SessionLocal()
    try:
        # Get the first user
        user = db.query(User).first()
        if not user:
            print("❌ No users found. Please register a user first.")
            return
        
        print(f"Creating quiz for user: {user.username} (ID: {user.id})")
        
        # Create proper questions with the exact format expected
        questions = [
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
        
        # Convert to JSON string
        questions_json = json.dumps(questions)
        print(f"Questions JSON: {questions_json}")
        
        # Create the quiz attempt
        quiz_attempt = QuizAttempt(
            user_id=user.id,
            topic="Test Resume Quiz",
            total_questions=3,
            questions_data=questions_json,
            status="incomplete",
            created_at=datetime.now(timezone.utc)
        )
        
        db.add(quiz_attempt)
        db.commit()
        db.refresh(quiz_attempt)
        
        print(f"✅ Created quiz attempt:")
        print(f"   ID: {quiz_attempt.id}")
        print(f"   Topic: {quiz_attempt.topic}")
        print(f"   Status: {quiz_attempt.status}")
        print(f"   User ID: {quiz_attempt.user_id}")
        
        # Verify the data can be parsed
        test_questions = json.loads(quiz_attempt.questions_data)
        print(f"✅ Verification: {len(test_questions)} questions can be parsed")
        print(f"   First question: {test_questions[0]['question']}")
        
        return quiz_attempt.id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    quiz_id = create_working_quiz()
    if quiz_id:
        print(f"\n🎯 Test this quiz by going to:")
        print(f"   Dashboard → Click Resume on 'Test Resume Quiz'")
        print(f"   Or test API: http://127.0.0.1:8000/api/quiz/{quiz_id}")