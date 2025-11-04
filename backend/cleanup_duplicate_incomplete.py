#!/usr/bin/env python3
"""
Clean up duplicate incomplete quizzes
"""

from database import SessionLocal, QuizAttempt
from sqlalchemy import func

def cleanup_duplicate_incomplete():
    """Remove duplicate incomplete quizzes for the same topic and user"""
    db = SessionLocal()
    try:
        print("🧹 Cleaning up duplicate incomplete quizzes...")
        
        # Get all incomplete quizzes grouped by user and topic
        incomplete_quizzes = db.query(QuizAttempt).filter(
            QuizAttempt.status == 'incomplete'
        ).order_by(QuizAttempt.user_id, QuizAttempt.topic, QuizAttempt.created_at.desc()).all()
        
        # Group by user_id and topic
        seen_combinations = set()
        to_delete = []
        
        for quiz in incomplete_quizzes:
            combination = (quiz.user_id, quiz.topic)
            
            if combination in seen_combinations:
                # This is a duplicate - mark for deletion
                print(f"🗑️  Marking duplicate for deletion: ID {quiz.id}, Topic: {quiz.topic}, User: {quiz.user_id}")
                to_delete.append(quiz)
            else:
                # This is the first (most recent) one for this combination - keep it
                seen_combinations.add(combination)
                print(f"✅ Keeping: ID {quiz.id}, Topic: {quiz.topic}, User: {quiz.user_id}")
        
        # Delete the duplicates
        deleted_count = 0
        for quiz in to_delete:
            db.delete(quiz)
            deleted_count += 1
        
        db.commit()
        
        print(f"\n✅ Cleanup completed!")
        print(f"   Deleted {deleted_count} duplicate incomplete quizzes")
        
        # Show remaining incomplete quizzes
        remaining = db.query(QuizAttempt).filter(QuizAttempt.status == 'incomplete').all()
        print(f"   Remaining incomplete quizzes: {len(remaining)}")
        
        for quiz in remaining:
            print(f"     - ID {quiz.id}: {quiz.topic} (User {quiz.user_id})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_duplicate_incomplete()