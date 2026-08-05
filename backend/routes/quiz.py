from fastapi import APIRouter, Request
from models.requests import QuizRequest
from models.responses import APIResponse, QuizData, create_success_response
from services.groq_service import groq_service
from services.prompts import build_quiz_prompt, QUIZ_SYSTEM_PROMPT
from utils.logger import get_logger
from utils.rate_limiter import limiter
from constants import RATE_LIMIT

logger = get_logger(__name__)
router = APIRouter(tags=["Quizzes"])

@router.post("/generate-quiz", response_model=APIResponse)
@limiter.limit(RATE_LIMIT)
async def generate_quiz(request: Request, quiz_request: QuizRequest):
    try:
        logger.info("Generating quiz for lesson plan")
        prompt = build_quiz_prompt(quiz_request.lesson_plan, quiz_request.num_questions)
        content, model_used = groq_service.generate_completion(prompt, QUIZ_SYSTEM_PROMPT)
        
        return create_success_response(
            message="Quiz generated successfully",
            data=QuizData(quiz=content),
            model_used=model_used
        )
    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}")
        raise e
