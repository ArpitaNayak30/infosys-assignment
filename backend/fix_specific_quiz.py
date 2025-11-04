#!/usr/bin/env python3
"""
Fix the specific quiz that's causing issues
"""

from database import SessionLocal, QuizAttempt
import json

def fix_quiz_42():
    """Fix quiz ID 42 specifically"""
    db = SessionLocal()
    try:
        # Get quiz ID 42
        quiz = db.query(QuizAttempt).filter(QuizAttempt.id == 42).first()
        
        if not quiz:
            print("❌ Quiz ID 42 not found")
            return
        
        print(f"Found quiz ID 42:")
        print(f"  Topic: {quiz.topic}")
        print(f"  Status: {quiz.status}")
        print(f"  Questions data: {quiz.questions_data}")
        
        # Create proper questions for history topic
        questions = [
            {
                "question": "In what year did World War II end?",
                "options": ["A) 1944", "B) 1945", "C) 1946", "D) 1947"]
            },
            {
                "question": "Who was the first President of the United States?",
                "options": ["A) Thomas Jefferson", "B) John Adams", "C) George Washington", "D) Benjamin Franklin"]
            },
            {
                "question": "Which ancient wonder of the world was located in Alexandria?",
                "options": ["A) Hanging Gardens", "B) Lighthouse of Alexandria", "C) Colossus of Rhodes", "D) Temple of Artemis"]
            },
            {
                "question": "The Renaissance period began in which country?",
                "options": ["A) France", "B) Germany", "C) Italy", "D) Spain"]
            },
            {
                "question": "Which empire was ruled by Julius Caesar?",
                "options": ["A) Greek Empire", "B) Roman Empire", "C) Persian Empire", "D) Egyptian Empire"]
            }
        ]
        
        # Update the quiz with proper data
        quiz.questions_data = json.dumps(questions)
        quiz.total_questions = len(questions)
        
        db.commit()
        
        print(f"✅ Fixed quiz ID 42!")
        print(f"  Added {len(questions)} history questions")
        print(f"  Questions data length: {len(quiz.questions_data)}")
        
        # Verify it works
        test_parse = json.loads(quiz.questions_data)
        print(f"✅ Verification: {len(test_parse)} questions parsed successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_quiz_42()