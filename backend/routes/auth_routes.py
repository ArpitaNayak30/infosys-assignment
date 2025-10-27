from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, User
from auth_models import UserRegister, UserLogin, LoginResponse, UserResponse, MessageResponse
from controllers.auth_controller import AuthController
from utils.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/auth", tags=["authentication"])
auth_controller = AuthController()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - **username**: Unique username (required)
    - **email**: Valid email address (required)
    - **password**: Password (required)
    """
    return await auth_controller.register_user(user_data, db)

@router.post("/login", response_model=LoginResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and get access token
    
    - **username**: Username (required)
    - **password**: Password (required)
    """
    return await auth_controller.login_user(user_data, db)

@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: User = Depends(get_current_active_user)):
    """
    Logout current user
    
    Note: In JWT stateless authentication, logout is handled client-side
    by removing the token from storage.
    """
    return await auth_controller.logout_user()

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    """
    Get current user profile
    
    Requires valid authentication token.
    """
    return await auth_controller.get_user_profile(current_user)