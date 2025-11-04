from http.client import HTTPException
from fastapi import APIRouter, Depends
from mysqlx import Session
from database import QuizAttempt, SessionLocal, get_db, User
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

import json
from fastapi import HTTPException

'''@router.get("/{quiz_id}")
async def get_quiz_by_id(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    quiz = db.query(QuizAttempt).filter(
        QuizAttempt.id == quiz_id,
        QuizAttempt.user_id == current_user.id
    ).first()

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if not quiz.questions_data:
        raise HTTPException(status_code=400, detail="No question data found")

    # Parse JSON safely
    try:
        questions = json.loads(quiz.questions_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid question data format")

    return {
        "id": quiz.id,
        "topic": quiz.topic,
        "questions_data": questions,
        "status": quiz.status,
        "score": quiz.score,
        "percentage": quiz.percentage,
    }'''
