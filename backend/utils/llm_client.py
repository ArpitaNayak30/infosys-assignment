import requests
import json
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    
    def generate_content(self, prompt: str) -> str:
    
        payload = json.dumps({
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                     }
                    ]
                }
            ]
        })

        headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.base_url, headers=headers, data=payload)
            response.raise_for_status()

            result = response.json()

            # Gemini response format fix
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected API response format: {str(e)}")


    def generate_questions(self, topic: str, number_questions: int) -> str:
        """Generate questions for a given topic"""
        prompt = f"""
    Generate {number_questions} multiple choice questions about {topic}.
    Each question should have 4 options (A, B, C, D).
    Format the response as valid JSON with this exact structure:
    {{
    "questions": [
        {{
        "question": "Question text here?",
        "options": ["Option A", "Option B", "Option C", "Option D"]
        }}
  ]
    "answers": [
        "Correct option for question 1",
        "Correct option for question 2",
        ...}}

    Make sure the questions are educational and the options are plausible but only one is correct.
    Topic: {topic}
    Number of questions: {number_questions}
    """
        return self.generate_content(prompt)