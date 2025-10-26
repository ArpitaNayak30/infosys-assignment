from fastapi import APIRouter
from models import GenerateQuestionsRequest, GenerateQuestionsResponse
from controllers.question_controller import QuestionController

router = APIRouter(prefix="/api", tags=["questions"])
question_controller = QuestionController()

@router.post("/generate-questions", response_model=GenerateQuestionsResponse)
async def generate_questions(request: GenerateQuestionsRequest):
    """
    Generate questions based on a topic
    
    - **topic**: The subject/topic for question generation
    - **number_questions**: Number of questions to generate (1-20)
    """
    return await question_controller.generate_questions(request)