import json
from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from database import get_db, QuizAttempt, User
from quiz_models import (
    QuizAttemptCreate, 
    QuizAttemptUpdate, 
    QuizAttemptResponse, 
    QuizStatsResponse,
    RecentQuizResponse,
    QuizStatus
)

class QuizController:
    
    async def create_quiz_attempt(
        self, 
        quiz_data: QuizAttemptCreate, 
        current_user: User,
        db: Session = Depends(get_db)
    ) -> QuizAttemptResponse:
        """Create a new quiz attempt"""
        try:
            # Calculate percentage if score is provided
            percentage = None
            completed_at = None
            
            if quiz_data.score is not None and quiz_data.status == QuizStatus.COMPLETED:
                percentage = (quiz_data.score / quiz_data.total_questions) * 100
                completed_at = datetime.now(timezone.utc)
            
            quiz_attempt = QuizAttempt(
                user_id=current_user.id,
                topic=quiz_data.topic,
                total_questions=quiz_data.total_questions,
                questions_data=json.dumps(quiz_data.questions_data),
                answers=json.dumps(quiz_data.answers) if quiz_data.answers else None,
                score=quiz_data.score,
                percentage=percentage,
                status=quiz_data.status.value,
                completed_at=completed_at
            )
            
            db.add(quiz_attempt)
            db.commit()
            db.refresh(quiz_attempt)
            
            return QuizAttemptResponse.model_validate(quiz_attempt)
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create quiz attempt: {str(e)}"
            )
    
    async def complete_quiz_attempt(
        self,
        quiz_id: int,
        quiz_update: QuizAttemptUpdate,
        current_user: User,
        db: Session = Depends(get_db)
    ) -> QuizAttemptResponse:
        """Complete a quiz attempt with answers and score"""
        try:
            quiz_attempt = db.query(QuizAttempt).filter(
                QuizAttempt.id == quiz_id,
                QuizAttempt.user_id == current_user.id
            ).first()
            
            if not quiz_attempt:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Quiz attempt not found"
                )
            
            # Calculate percentage
            percentage = (quiz_update.score / quiz_update.total_questions) * 100
            
            # Update quiz attempt
            quiz_attempt.answers = json.dumps(quiz_update.answers)
            quiz_attempt.score = quiz_update.score
            quiz_attempt.percentage = percentage
            quiz_attempt.status = quiz_update.status.value
            quiz_attempt.completed_at = datetime.now(timezone.utc)
            
            db.commit()
            db.refresh(quiz_attempt)
            
            return QuizAttemptResponse.model_validate(quiz_attempt)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to complete quiz: {str(e)}"
            )
    
    async def get_user_quiz_stats(
        self,
        current_user: User,
        db: Session = Depends(get_db)
    ) -> QuizStatsResponse:
        """Get quiz statistics for the current user"""
        try:
            # Get all quiz attempts for user
            total_quizzes = db.query(QuizAttempt).filter(
                QuizAttempt.user_id == current_user.id
            ).count()
            
            completed_quizzes = db.query(QuizAttempt).filter(
                QuizAttempt.user_id == current_user.id,
                QuizAttempt.status == "completed"
            ).count()
            
            incomplete_quizzes = total_quizzes - completed_quizzes
            
            # Get score statistics for completed quizzes
            completed_attempts = db.query(QuizAttempt).filter(
                QuizAttempt.user_id == current_user.id,
                QuizAttempt.status == "completed"
            ).all()
            
            if completed_attempts:
                scores = [attempt.score for attempt in completed_attempts]
                percentages = [attempt.percentage for attempt in completed_attempts]
                
                average_score = sum(scores) / len(scores)
                highest_score = max(scores)
                lowest_score = min(scores)
                average_percentage = sum(percentages) / len(percentages)
            else:
                average_score = 0
                highest_score = 0
                lowest_score = 0
                average_percentage = 0
            
            return QuizStatsResponse(
                total_quizzes=total_quizzes,
                completed_quizzes=completed_quizzes,
                incomplete_quizzes=incomplete_quizzes,
                average_score=round(average_score, 2),
                highest_score=highest_score,
                lowest_score=lowest_score,
                average_percentage=round(average_percentage, 2)
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get quiz stats: {str(e)}"
            )
    
    async def get_recent_quizzes(
        self,
        current_user: User,
        limit: int = 10,
        db: Session = Depends(get_db)
    ) -> RecentQuizResponse:
        """Get recent quiz attempts for the current user"""
        try:
            # Get recent quiz attempts
            recent_quizzes = db.query(QuizAttempt).filter(
                QuizAttempt.user_id == current_user.id
            ).order_by(desc(QuizAttempt.created_at)).limit(limit).all()
            
            quiz_responses = [
                QuizAttemptResponse.model_validate(quiz) 
                for quiz in recent_quizzes
            ]
            
            # Get stats
            stats = await self.get_user_quiz_stats(current_user, db)
            
            return RecentQuizResponse(
                quizzes=quiz_responses,
                stats=stats
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get recent quizzes: {str(e)}"
            )
    
    async def get_quiz_attempt(
        self,
        quiz_id: int,
        current_user: User,
        db: Session = Depends(get_db)
    ) -> QuizAttemptResponse:
        """Get a specific quiz attempt"""
        try:
            quiz_attempt = db.query(QuizAttempt).filter(
                QuizAttempt.id == quiz_id,
                QuizAttempt.user_id == current_user.id
            ).first()
            
            if not quiz_attempt:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Quiz attempt not found"
                )
            
            return QuizAttemptResponse.model_validate(quiz_attempt)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get quiz attempt: {str(e)}"
            )