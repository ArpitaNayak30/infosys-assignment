from pydantic import BaseModel
from email_validator import validate_email, EmailNotValidError
from typing import Optional
from datetime import datetime

# Request models
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    
    def validate_email_format(self):
        try:
            validate_email(self.email)
            return True
        except EmailNotValidError:
            return False
    
    def validate_password(self):
        # Check password length (bcrypt has 72 byte limit)
        if len(self.password.encode('utf-8')) > 72:
            return False, "Password is too long (max 72 bytes)"
        
        # Check minimum length
        if len(self.password) < 6:
            return False, "Password must be at least 6 characters long"
        
        return True, "Password is valid"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Response models
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class MessageResponse(BaseModel):
    message: str