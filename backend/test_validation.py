#!/usr/bin/env python3
"""
Test validation functions
"""

from auth_models import UserRegister

def test_validation():
    """Test the validation functions"""
    print("🧪 Testing validation functions...")
    
    # Test data
    test_user = UserRegister(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    
    print(f"📧 Testing email validation for: {test_user.email}")
    try:
        email_valid = test_user.validate_email_format()
        print(f"✅ Email validation result: {email_valid}")
    except Exception as e:
        print(f"❌ Email validation failed: {e}")
    
    print(f"🔒 Testing password validation for: {test_user.password}")
    try:
        password_valid, password_message = test_user.validate_password()
        print(f"✅ Password validation result: {password_valid}, message: {password_message}")
    except Exception as e:
        print(f"❌ Password validation failed: {e}")

if __name__ == "__main__":
    test_validation()