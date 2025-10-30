#!/usr/bin/env python3
"""
Database migration script to add quiz tracking tables
"""

from database import create_tables, engine, Base
from sqlalchemy import text

def migrate_database():
    """Add new tables for quiz tracking"""
    try:
        print("🚀 Migrating database...")
        
        # Create all tables (will only create new ones)
        create_tables()
        
        print("✅ Database migration completed successfully!")
        print("📊 Quiz tracking tables are now available")
        
        # Test database connection
        from database import SessionLocal
        db = SessionLocal()
        try:
            # Check if quiz_attempts table exists
            result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='quiz_attempts'")).fetchone()
            if result:
                print("✅ Quiz attempts table created successfully!")
            else:
                print("⚠️  Quiz attempts table not found")
        except Exception as e:
            print(f"⚠️  Database test failed: {e}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database migration failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    migrate_database()