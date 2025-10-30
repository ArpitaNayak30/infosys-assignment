from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class QuizStatus(str, Enum):
    INCOMPLETE = "incomplete"
    COMPLETED = "completed"

class QuizAttemptCreate(BaseModel):
    topic: str
    total_questions: int
    questions_data: List[dict]  # Store the questions and options
    status: QuizStatus = QuizStatus.INCOMPLETE

class QuizAttemptUpdate(BaseModel):
    answers: List[dict]  # User's answers
    score: int
    total_questions: int
    status: QuizStatus = QuizStatus.COMPLETED

class QuizAttemptResponse(BaseModel):
    id: int
    user_id: int
    topic: str
    total_questions: int
    score: Optional[int] = None
    percentage: Optional[float] = None
    status: QuizStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}

class QuizStatsResponse(BaseModel):
    total_quizzes: int
    completed_quizzes: int
    incomplete_quizzes: int
    average_score: float
    highest_score: int
    lowest_score: int
    average_percentage: float

class RecentQuizResponse(BaseModel):
    quizzes: List[QuizAttemptResponse]
    stats: QuizStatsResponse