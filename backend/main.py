
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.question_routes import router as question_router
from routes.auth_routes import router as auth_router
from database import create_tables

# Create database tables on startup
create_tables()

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

@app.get("/")
def hello():
    return {"message": "Question Generator API with Authentication is running!"}

