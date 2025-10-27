#!/usr/bin/env python3
"""
Database setup script for Question Generator API
This script creates the MySQL database and tables
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create the MySQL database if it doesn't exist"""
    try:
        # Database connection parameters
        host = "localhost"
        user = "root"
        password = "Arpita@123"  # Empty password for root user
        database_name = "question_generator"
        
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"✅ Database '{database_name}' created successfully (or already exists)")
            
            # Create user table (optional, SQLAlchemy will handle this)
            cursor.execute(f"USE {database_name}")
            
            cursor.close()
            connection.close()
            print("✅ Database setup completed successfully")
            
    except Error as e:
        print(f"❌ Error creating database: {e}")
        print("\n💡 Make sure:")
        print("1. MySQL server is running")
        print("2. Root password is correct")
        print("3. You have permission to create databases")

def main():
    """Main setup function"""
    print("🚀 Setting up Question Generator Database")
    print("=" * 50)
    
    create_database()
    
    print("\n📋 Next steps:")
    print("1. Update your .env file with correct database credentials")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the API: uvicorn main:app --reload")
    print("4. The API will automatically create the user tables on startup")

if __name__ == "__main__":
    main()