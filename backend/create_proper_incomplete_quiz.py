#!/usr/bin/env python3
"""
Create a proper incomplete quiz with valid question data
"""

from database import SessionLocal, QuizAttempt, User
import json
from datetime import datetime, timezone

def create_proper_quiz():
    """Create a proper incomplete quiz"""
    db = SessionLocal()
    try:
        # Get the first user
        user = db.query(User).first()
        if not user:
            print("❌ No users found. Please register a user first.")
            return
        
        # Delete existing broken incomplete quizzes
        broken_quizzes = db.query(QuizAttempt).filter(
            QuizAttempt.status == 'incomplete'
        ).all()
        
        for quiz in broken_quizzes:
            print(f"🗑️  Deleting broken quiz ID: {quiz.id}")
            db.delete(quiz)
        
        # Create proper questions
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
            },
            {
                "question": "Who wrote Romeo and Juliet?",
                "options": ["A) Charles Dickens", "B) William Shakespeare", "C) Jane Austen", "D) Mark Twain"]
            },
            {
                "question": "What is the largest ocean on Earth?",
                "options": ["A) Atlantic", "B) Indian", "C) Arctic", "D) Pacific"]
            }
        ]
        
        # Create new incomplete quiz with proper data
        quiz_attempt = QuizAttempt(
            user_id=user.id,
            topic="General Knowledge",
            total_questions=5,
            questions_data=json.dumps(questions),  # Proper JSON string
            status="incomplete",
            created_at=datetime.now(timezone.utc)
        )
        
        db.add(quiz_attempt)
        db.commit()
        db.refresh(quiz_attempt)
        
        print(f"✅ Created proper incomplete quiz!")
        print(f"   ID: {quiz_attempt.id}")
        print(f"   Topic: {quiz_attempt.topic}")
        print(f"   Questions: {len(questions)}")
        print(f"   Status: {quiz_attempt.status}")
        
        # Verify the JSON is valid
        test_parse = json.loads(quiz_attempt.questions_data)
        print(f"✅ JSON verification: {len(test_parse)} questions parsed successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_proper_quiz()