from fastapi import APIRouter, Depends
from models import GenerateQuestionsRequest, GenerateQuestionsResponse
from controllers.question_controller import QuestionController
from utils.auth_utils import get_current_active_user
from database import User

router = APIRouter(prefix="/api", tags=["questions"])
question_controller = QuestionController()

@router.post("/generate-questions", response_model=GenerateQuestionsResponse)
async def generate_questions(
    request: GenerateQuestionsRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate questions based on a topic (Requires Authentication)
    
    - **topic**: The subject/topic for question generation
    - **number_questions**: Number of questions to generate (1-20)
    """
    return await question_controller.generate_questions(request)