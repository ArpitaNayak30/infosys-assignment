from fastapi import APIRouter, Depends
from database import get_db, User
from utils.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/quiz", tags=["quiz"])

@router.get("/recent")
async def get_recent_quizzes(
    current_user: User = Depends(get_current_active_user)
):
    """Get recent quiz attempts - simplified version"""
    # Return empty data for now
    return {
        "quizzes": [],
        "stats": {
            "total_quizzes": 0,
            "completed_quizzes": 0,
            "incomplete_quizzes": 0,
            "average_score": 0.0,
            "highest_score": 0,
            "lowest_score": 0,
            "average_percentage": 0.0
        }
    }

@router.get("/stats")
async def get_quiz_stats(
    current_user: User = Depends(get_current_active_user)
):
    """Get quiz statistics - simplified version"""
    return {
        "total_quizzes": 0,
        "completed_quizzes": 0,
        "incomplete_quizzes": 0,
        "average_score": 0.0,
        "highest_score": 0,
        "lowest_score": 0,
        "average_percentage": 0.0
    }