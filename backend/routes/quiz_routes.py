from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, User
from quiz_models import (
    QuizAttemptCreate,
    QuizAttemptUpdate, 
    QuizAttemptResponse,
    QuizStatsResponse,
    RecentQuizResponse
)
from controllers.quiz_controller import QuizController
from utils.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/quiz", tags=["quiz"])
quiz_controller = QuizController()

@router.post("/start", response_model=QuizAttemptResponse, status_code=201)
async def start_quiz(
    quiz_data: QuizAttemptCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Start a new quiz attempt
    
    - **topic**: Quiz topic
    - **total_questions**: Number of questions
    - **questions_data**: Array of questions with options
    """
    return await quiz_controller.create_quiz_attempt(quiz_data, current_user, db)

@router.put("/{quiz_id}/complete", response_model=QuizAttemptResponse)
async def complete_quiz(
    quiz_id: int,
    quiz_update: QuizAttemptUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Complete a quiz attempt with answers and score
    
    - **quiz_id**: ID of the quiz attempt
    - **answers**: User's answers
    - **score**: Final score
    - **total_questions**: Total number of questions
    """
    return await quiz_controller.complete_quiz_attempt(quiz_id, quiz_update, current_user, db)

@router.get("/stats", response_model=QuizStatsResponse)
async def get_quiz_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get quiz statistics for the current user
    
    Returns total quizzes, completed, incomplete, average score, etc.
    """
    return await quiz_controller.get_user_quiz_stats(current_user, db)

@router.get("/recent", response_model=RecentQuizResponse)
async def get_recent_quizzes(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get recent quiz attempts for the current user
    
    - **limit**: Number of recent quizzes to return (default: 10)
    """
    return await quiz_controller.get_recent_quizzes(current_user, limit, db)

@router.get("/{quiz_id}", response_model=QuizAttemptResponse)
async def get_quiz_attempt(
    quiz_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific quiz attempt
    
    - **quiz_id**: ID of the quiz attempt
    """
    return await quiz_controller.get_quiz_attempt(quiz_id, current_user, db)