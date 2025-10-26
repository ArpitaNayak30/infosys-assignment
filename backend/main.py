
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.question_routes import router as question_router

app = FastAPI(
    title="Question Generator API",
    description="API for generating educational questions using AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(question_router)

@app.get("/")
def hello():
    return {"message": "hello"}

