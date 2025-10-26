from pydantic import BaseModel
from typing import List

class GenerateQuestionsRequest(BaseModel):
    topic: str
    number_questions: int

class QuestionOption(BaseModel):
    question: str
    options: List[str]

class GenerateQuestionsResponse(BaseModel):
    questions: List[QuestionOption]