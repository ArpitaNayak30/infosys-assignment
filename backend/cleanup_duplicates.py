#!/usr/bin/env python3
"""
Clean up duplicate quiz attempts
"""

from database import SessionLocal, QuizAttempt
from sqlalchemy import func

def cleanup_duplicates():
    """Remove duplicate incomplete quiz attempts"""
    db = SessionLocal()
    try:
        print("🧹 Cleaning up duplicate quiz attempts...")
        
        # Delete incomplete attempts that have a corresponding completed attempt
        # for the same user, topic, and similar timestamp
        
        # First, let's see what we have
        total_attempts = db.query(QuizAttempt).count()
        incomplete_attempts = db.query(QuizAttempt).filter(QuizAttempt.status == 'incomplete').count()
        completed_attempts = db.query(QuizAttempt).filter(QuizAttempt.status == 'completed').count()
        
        print(f"📊 Current state:")
        print(f"   Total attempts: {total_attempts}")
        print(f"   Incomplete: {incomplete_attempts}")
        print(f"   Completed: {completed_attempts}")
        
        # Delete incomplete attempts where there's a completed attempt for the same user and topic
        deleted_count = 0
        
        # Get all incomplete attempts
        incomplete = db.query(QuizAttempt).filter(QuizAttempt.status == 'incomplete').all()
        
        for inc_attempt in incomplete:
            # Check if there's a completed attempt for the same user and topic
            completed_exists = db.query(QuizAttempt).filter(
                QuizAttempt.user_id == inc_attempt.user_id,
                QuizAttempt.topic == inc_attempt.topic,
                QuizAttempt.status == 'completed',
                QuizAttempt.created_at >= inc_attempt.created_at
            ).first()
            
            if completed_exists:
                print(f"🗑️  Deleting incomplete attempt: {inc_attempt.topic} (ID: {inc_attempt.id})")
                db.delete(inc_attempt)
                deleted_count += 1
        
        db.commit()
        
        # Show final state
        final_total = db.query(QuizAttempt).count()
        final_incomplete = db.query(QuizAttempt).filter(QuizAttempt.status == 'incomplete').count()
        final_completed = db.query(QuizAttempt).filter(QuizAttempt.status == 'completed').count()
        
        print(f"\n✅ Cleanup completed!")
        print(f"   Deleted {deleted_count} duplicate incomplete attempts")
        print(f"   Final state:")
        print(f"   Total attempts: {final_total}")
        print(f"   Incomplete: {final_incomplete}")
        print(f"   Completed: {final_completed}")
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_duplicates()