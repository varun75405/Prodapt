from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from constants import API_TITLE, API_DESCRIPTION, API_VERSION
from utils.rate_limiter import limiter
from utils.exceptions import GroqAPIError, GroqRateLimitError, GroqEmptyResponseError
from utils.exceptions import groq_api_error_handler, generic_error_handler
from utils.logger import get_logger
from routes import auth, lesson, quiz, material, simplify, activity

logger = get_logger(__name__)

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS - allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handlers
app.add_exception_handler(GroqAPIError, groq_api_error_handler)
app.add_exception_handler(GroqRateLimitError, groq_api_error_handler)
app.add_exception_handler(GroqEmptyResponseError, groq_api_error_handler)
app.add_exception_handler(Exception, generic_error_handler)

# Include routers
app.include_router(auth.router)
app.include_router(lesson.router)
app.include_router(quiz.router)
app.include_router(material.router)
app.include_router(simplify.router)
app.include_router(activity.router)

@app.get("/", tags=["Health"])
async def health_check():
    return {
        "success": True, 
        "message": "API is running", 
        "data": {"service": "AI Teacher's Assistant API", "version": API_VERSION}, 
        "model_used": None
    }

logger.info(f"{API_TITLE} v{API_VERSION} initialized")

if __name__ == "__main__":
    import uvicorn
    from config import BACKEND_HOST, BACKEND_PORT
    uvicorn.run("main:app", host=BACKEND_HOST, port=int(BACKEND_PORT), reload=True)
