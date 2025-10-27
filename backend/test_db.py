#!/usr/bin/env python3
"""
Test database operations directly
"""

from database import SessionLocal, User, create_tables
from utils.auth_utils import get_password_hash
from datetime import datetime

def test_database():
    """Test database operations"""
    print("🧪 Testing database operations...")
    
    # Ensure tables exist
    create_tables()
    
    db = SessionLocal()
    try:
        # Test creating a user directly
        print("📝 Creating test user...")
        
        test_user = User(
            username="testuser_direct",
            email="test_direct@example.com",
            hashed_password=get_password_hash("password123"),
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"✅ User created successfully with ID: {test_user.id}")
        
        # Test querying the user
        found_user = db.query(User).filter(User.username == "testuser_direct").first()
        if found_user:
            print(f"✅ User found: {found_user.username} ({found_user.email})")
        else:
            print("❌ User not found")
            
        # Clean up
        db.delete(test_user)
        db.commit()
        print("🧹 Test user cleaned up")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_database()