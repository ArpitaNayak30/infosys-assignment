
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.question_routes import router as question_router
from routes.auth_routes import router as auth_router
from database import create_tables

# Create database tables on startup
create_tables()

# Try to import quiz routes with error handling
try:
    from routes.quiz_routes import router as quiz_router
    QUIZ_ROUTES_LOADED = True
    print("✅ Quiz routes loaded successfully")
except Exception as e:
    print(f"❌ Failed to load quiz routes: {e}")
    print("🔄 Loading simple quiz routes as fallback")
    try:
        from simple_quiz_routes import router as quiz_router
        QUIZ_ROUTES_LOADED = True
        print("✅ Simple quiz routes loaded successfully")
    except Exception as e2:
        print(f"❌ Failed to load simple quiz routes: {e2}")
        QUIZ_ROUTES_LOADED = False

app = FastAPI(
    title="Question Generator API with Authentication",
    description="API for generating educational questions using AI with user authentication",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(question_router)

# Only include quiz router if it loaded successfully
if QUIZ_ROUTES_LOADED:
    app.include_router(quiz_router)
    print("✅ Quiz routes included in app")
else:
    print("⚠️ Quiz routes not included due to import error")

@app.get("/")
def hello():
    return {"message": "Question Generator API with Authentication is running!"}

@app.get("/test")
def test():
    return {
        "message": "Test endpoint working", 
        "quiz_routes_loaded": QUIZ_ROUTES_LOADED,
        "available_routes": ["auth", "questions", "quiz" if QUIZ_ROUTES_LOADED else "quiz_disabled"]
    }

@app.get("/test-quiz")
def test_quiz():
    """Test if quiz routes are accessible"""
    try:
        from database import SessionLocal, QuizAttempt
        db = SessionLocal()
        # Try to query the quiz_attempts table
        count = db.query(QuizAttempt).count()
        db.close()
        return {"message": "Quiz database working", "quiz_attempts_count": count}
    except Exception as e:
        return {"message": "Quiz database error", "error": str(e)}
    

