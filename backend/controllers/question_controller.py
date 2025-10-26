import json
from fastapi import HTTPException
from models import GenerateQuestionsRequest, GenerateQuestionsResponse
from utils.llm_client import GeminiClient

class QuestionController:
    def __init__(self):
        self.llm_client = GeminiClient()
    
    async def generate_questions(self, request: GenerateQuestionsRequest) -> GenerateQuestionsResponse:
        """Generate questions based on topic and number requested"""
        try:
            # Validate input
            if not request.topic.strip():
                raise HTTPException(status_code=400, detail="Topic cannot be empty")
            
            if request.number_questions <= 0 or request.number_questions > 20:
                raise HTTPException(status_code=400, detail="Number of questions must be between 1 and 20")
            
            # Generate questions using LLM
            llm_response = self.llm_client.generate_questions(request.topic, request.number_questions)
            
            # Parse the JSON response from LLM
            try:
                questions_data = json.loads(llm_response)
                return GenerateQuestionsResponse(**questions_data)
            except json.JSONDecodeError:
                # If LLM doesn't return valid JSON, try to extract it
                cleaned_response = self._clean_json_response(llm_response)
                questions_data = json.loads(cleaned_response)
                return GenerateQuestionsResponse(**questions_data)
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate questions: {str(e)}")
    
    def _clean_json_response(self, response: str) -> str:
        """Clean and extract JSON from LLM response"""
        # Remove markdown code blocks if present
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            response = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            response = response[start:end].strip()
        
        # Find JSON object boundaries
        start_idx = response.find("{")
        end_idx = response.rfind("}") + 1
        
        if start_idx != -1 and end_idx != 0:
            return response[start_idx:end_idx]
        
        return response