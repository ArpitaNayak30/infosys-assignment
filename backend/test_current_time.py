#!/usr/bin/env python3
"""
Test current time storage and retrieval
"""

from database import SessionLocal, QuizAttempt, User
import json
from datetime import datetime, timezone

def test_current_time():
    """Test storing current time"""
    db = SessionLocal()
    try:
        user = db.query(User).first()
        if not user:
            print("❌ No users found")
            return
        
        # Get current time
        current_time = datetime.now(timezone.utc)
        print(f"Current UTC time: {current_time}")
        print(f"Current local time: {datetime.now()}")
        
        # Create a quiz with current time
        questions = [{"question": "Test?", "options": ["A", "B", "C", "D"]}]
        
        quiz = QuizAttempt(
            user_id=user.id,
            topic="Time Test",
            total_questions=1,
            questions_data=json.dumps(questions),
            status="completed",
            score=1,
            percentage=100.0,
            created_at=current_time,
            completed_at=current_time
        )
        
        db.add(quiz)
        db.commit()
        db.refresh(quiz)
        
        print(f"✅ Created quiz with ID: {quiz.id}")
        print(f"Stored created_at: {quiz.created_at}")
        print(f"Stored completed_at: {quiz.completed_at}")
        
        # Test how it looks when retrieved
        retrieved = db.query(QuizAttempt).filter(QuizAttempt.id == quiz.id).first()
        print(f"Retrieved created_at: {retrieved.created_at}")
        print(f"Retrieved type: {type(retrieved.created_at)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_current_time()