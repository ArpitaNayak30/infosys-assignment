from datetime import timedelta
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db, User
from auth_models import UserRegister, UserLogin, LoginResponse, UserResponse, MessageResponse
from utils.auth_utils import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES
)

class AuthController:
    
    async def register_user(self, user_data: UserRegister, db: Session = Depends(get_db)) -> UserResponse:
        """Register a new user"""
        try:
            # Validate email format
            if not user_data.validate_email_format():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid email format"
                )
            
            # Validate password
            password_valid, password_message = user_data.validate_password()
            if not password_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=password_message
                )
            
            # Check if user already exists
            existing_user = db.query(User).filter(
                (User.username == user_data.username) | (User.email == user_data.email)
            ).first()
            
            if existing_user:
                if existing_user.username == user_data.username:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username already registered"
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                    )
            
            # Hash password
            hashed_password = get_password_hash(user_data.password)
            
            # Create new user
            db_user = User(
                username=user_data.username,
                email=user_data.email,
                hashed_password=hashed_password
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            return UserResponse.model_validate(db_user)
            
        except HTTPException:
            # Re-raise HTTPExceptions as they are (don't wrap them)
            db.rollback()
            raise
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username or email already exists"
            )
        except Exception as e:
            db.rollback()
            print(f"Registration error type: {type(e)}")
            print(f"Registration error message: {str(e)}")
            print(f"Registration error repr: {repr(e)}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            
            error_msg = str(e) if str(e) else f"Unknown error: {type(e).__name__}"
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Registration failed: {error_msg}"
            )
    
    async def login_user(self, user_data: UserLogin, db: Session = Depends(get_db)) -> LoginResponse:
        """Authenticate user and return token"""
        # Find user by username
        user = db.query(User).filter(User.username == user_data.username).first()
        
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )
    
    async def logout_user(self) -> MessageResponse:
        """Logout user (client-side token removal)"""
        # In a stateless JWT system, logout is handled client-side
        # For more security, you could implement a token blacklist
        return MessageResponse(message="Successfully logged out")
    
    async def get_user_profile(self, current_user: User) -> UserResponse:
        """Get current user profile"""
        return UserResponse.model_validate(current_user)