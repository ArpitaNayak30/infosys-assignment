#!/usr/bin/env python3
"""
Initialize the database and create tables
"""

from database import create_tables, engine, Base
import os

def init_database():
    """Initialize the database and create all tables"""
    try:
        print("🚀 Initializing database...")
        
        # Create all tables
        create_tables()
        
        print("✅ Database initialized successfully!")
        print(f"📁 Database file: {os.path.abspath('question_generator.db')}")
        
        # Test database connection
        from database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        try:
            # Simple test query
            result = db.execute(text("SELECT 1")).fetchone()
            print("✅ Database connection test successful!")
        except Exception as e:
            print(f"⚠️  Database connection test failed: {e}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    init_database()