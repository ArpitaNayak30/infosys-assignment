#!/usr/bin/env python3
"""
Debug quiz data to see what's stored in questions_data
"""

from database import SessionLocal, QuizAttempt

def debug_quiz_data():
    """Check what's stored in questions_data"""
    db = SessionLocal()
    try:
        # Get incomplete quizzes
        incomplete_quizzes = db.query(QuizAttempt).filter(
            QuizAttempt.status == 'incomplete'
        ).all()
        
        print(f"Found {len(incomplete_quizzes)} incomplete quizzes:")
        
        for quiz in incomplete_quizzes:
            print(f"\n--- Quiz ID: {quiz.id} ---")
            print(f"Topic: {quiz.topic}")
            print(f"Status: {quiz.status}")
            print(f"Questions data type: {type(quiz.questions_data)}")
            print(f"Questions data length: {len(str(quiz.questions_data)) if quiz.questions_data else 'None'}")
            print(f"Questions data preview: {str(quiz.questions_data)[:100]}...")
            
            # Try to parse it
            if quiz.questions_data:
                try:
                    import json
                    parsed = json.loads(quiz.questions_data)
                    print(f"✅ JSON is valid, contains {len(parsed)} items")
                except Exception as e:
                    print(f"❌ JSON parsing failed: {e}")
            else:
                print("❌ questions_data is None/empty")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_quiz_data()