#!/usr/bin/env python3
"""
Fix broken quiz data in the database
"""

from database import SessionLocal, QuizAttempt
import json

def fix_quiz_data():
    """Fix broken questions_data in quiz attempts"""
    db = SessionLocal()
    try:
        # Get all quiz attempts with problematic data
        all_quizzes = db.query(QuizAttempt).all()
        
        fixed_count = 0
        deleted_count = 0
        
        for quiz in all_quizzes:
            print(f"\n--- Checking Quiz ID: {quiz.id} ---")
            print(f"Topic: {quiz.topic}")
            print(f"Status: {quiz.status}")
            
            if not quiz.questions_data or quiz.questions_data in ['undefined', 'null', '']:
                print(f"❌ Invalid questions_data: {quiz.questions_data}")
                
                if quiz.status == 'incomplete':
                    # Delete incomplete quizzes with no valid data
                    print(f"🗑️  Deleting incomplete quiz with invalid data")
                    db.delete(quiz)
                    deleted_count += 1
                else:
                    # For completed quizzes, create dummy data
                    dummy_questions = [
                        {
                            "question": f"Sample question for {quiz.topic}",
                            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"]
                        }
                    ]
                    quiz.questions_data = json.dumps(dummy_questions)
                    print(f"🔧 Fixed with dummy data")
                    fixed_count += 1
            else:
                try:
                    # Test if it's valid JSON
                    parsed = json.loads(quiz.questions_data)
                    print(f"✅ Valid JSON with {len(parsed)} questions")
                except:
                    print(f"❌ Invalid JSON, fixing...")
                    # Create dummy data for broken JSON
                    dummy_questions = [
                        {
                            "question": f"Sample question for {quiz.topic}",
                            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"]
                        }
                    ]
                    quiz.questions_data = json.dumps(dummy_questions)
                    fixed_count += 1
        
        db.commit()
        print(f"\n✅ Cleanup completed!")
        print(f"   Fixed: {fixed_count} quizzes")
        print(f"   Deleted: {deleted_count} incomplete quizzes")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_quiz_data()