# Question Generator API

A FastAPI-based REST API that generates educational quiz questions using Google's Gemini AI. The API allows users to specify a topic and number of questions, then returns AI-generated multiple-choice questions.

## 🚀 Features

- **AI-Powered Question Generation**: Uses Google Gemini 2.5 Flash model
- **Customizable Topics**: Generate questions on any subject
- **Flexible Question Count**: Request 1-20 questions per API call
- **Multiple Choice Format**: Each question includes 4 answer options
- **Input Validation**: Comprehensive request validation and error handling
- **CORS Enabled**: Ready for frontend integration
- **Auto-Generated Documentation**: Interactive API docs with Swagger UI

## 📋 Requirements

- Python 3.8+
- Google API Key for Gemini
- Internet connection for AI model access

## 🛠️ Installation

1. **Clone the repository and navigate to backend:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env and add your Google API key
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Get Google API Key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

## 🚦 Running the Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: `http://127.0.0.1:8000`
- **Interactive Docs**: `http://127.0.0.1:8000/docs`
- **OpenAPI Schema**: `http://127.0.0.1:8000/openapi.json`

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "message": "Question Generator API is running!"
}
```

#### 2. Generate Questions
```http
POST /api/generate-questions
```

**Request Body:**
```json
{
  "topic": "string",
  "number_questions": integer
}
```

**Parameters:**
- `topic` (string, required): The subject/topic for question generation
- `number_questions` (integer, required): Number of questions to generate (1-20)

**Example Request:**
```json
{
  "topic": "Chemistry",
  "number_questions": 5
}
```

**Success Response (200):**
```json
{
  "questions": [
    {
      "question": "Which of the following is an example of a chemical change?",
      "options": [
        "Melting ice",
        "Boiling water", 
        "Rusting iron",
        "Dissolving sugar"
      ]
    },
    {
      "question": "What is the chemical symbol for gold?",
      "options": [
        "Go",
        "Gd",
        "Au",
        "Ag"
      ]
    }
  ]
}
```

**Error Responses:**

- **400 Bad Request**: Invalid input parameters
  ```json
  {
    "detail": "Topic cannot be empty"
  }
  ```

- **500 Internal Server Error**: AI generation or server error
  ```json
  {
    "detail": "Failed to generate questions: API request failed"
  }
  ```

## 🧪 Testing the API

### Using the Test Script
```bash
python test_api.py
```

### Using cURL
```bash
# Generate 3 chemistry questions
curl -X POST http://127.0.0.1:8000/api/generate-questions \
  -H "Content-Type: application/json" \
  -d '{"topic": "Chemistry", "number_questions": 3}'

# Generate 5 history questions  
curl -X POST http://127.0.0.1:8000/api/generate-questions \
  -H "Content-Type: application/json" \
  -d '{"topic": "World History", "number_questions": 5}'
```

### Using Python requests
```python
import requests

url = "http://127.0.0.1:8000/api/generate-questions"
payload = {
    "topic": "Physics",
    "number_questions": 4
}

response = requests.post(url, json=payload)
data = response.json()

for i, question in enumerate(data['questions'], 1):
    print(f"Q{i}: {question['question']}")
    for j, option in enumerate(question['options'], 1):
        print(f"  {j}. {option}")
```

### Using JavaScript/Fetch
```javascript
const response = await fetch('http://127.0.0.1:8000/api/generate-questions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    topic: 'Mathematics',
    number_questions: 3
  })
});

const data = await response.json();
console.log(data.questions);
```

## 🏗️ Project Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── models.py                  # Pydantic models for request/response
├── requirements.txt           # Python dependencies
├── test_api.py               # API test script
├── .env                      # Environment variables (create from .env.example)
├── .env.example              # Environment variables template
├── routes/
│   ├── __init__.py
│   └── question_routes.py    # API route definitions
├── controllers/
│   ├── __init__.py
│   └── question_controller.py # Business logic
└── utils/
    ├── __init__.py
    └── llm_client.py         # Gemini AI client
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | Yes | None |

### API Limits

- **Maximum questions per request**: 20
- **Minimum questions per request**: 1
- **Topic length**: Must be non-empty string
- **Rate limiting**: None (consider implementing for production)

## 🔧 Development

### Adding New Features

1. **Models**: Add new Pydantic models in `models.py`
2. **Routes**: Add new endpoints in `routes/`
3. **Controllers**: Add business logic in `controllers/`
4. **Utils**: Add utility functions in `utils/`

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for functions and classes
- Handle exceptions appropriately

## 🚨 Error Handling

The API includes comprehensive error handling:

- **Input Validation**: Validates request parameters
- **AI API Errors**: Handles Gemini API failures gracefully  
- **JSON Parsing**: Handles malformed AI responses
- **Network Errors**: Manages connection issues
- **Rate Limiting**: Ready for rate limiting implementation

## 🔒 Security Considerations

- **API Key Security**: Store in environment variables, never in code
- **Input Sanitization**: Validate all user inputs
- **CORS**: Currently allows all origins (configure for production)
- **Rate Limiting**: Consider implementing for production use
- **HTTPS**: Use HTTPS in production environments

## 📈 Performance

- **Response Time**: Typically 2-5 seconds depending on question count
- **Concurrent Requests**: FastAPI handles concurrent requests efficiently
- **Caching**: Consider implementing response caching for repeated topics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **"GOOGLE_API_KEY environment variable is not set"**
   - Ensure `.env` file exists with valid API key
   - Check API key is active in Google AI Studio

2. **"Cannot connect to API"**
   - Verify server is running: `uvicorn main:app --reload`
   - Check port 8000 is not in use by another application

3. **"Failed to generate questions"**
   - Check internet connection
   - Verify Google API key has proper permissions
   - Check Gemini API service status

4. **Import errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Ensure Python 3.8+ is being used

### Getting Help

- Check the interactive API documentation at `/docs`
- Run the test script to verify setup: `python test_api.py`
- Review server logs for detailed error messages