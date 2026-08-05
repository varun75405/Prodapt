from fastapi import APIRouter, Request
from models.requests import LessonRequest
from models.responses import APIResponse, LessonData, create_success_response
from services.groq_service import groq_service
from services.prompts import build_lesson_prompt, LESSON_SYSTEM_PROMPT
from utils.logger import get_logger
from utils.rate_limiter import limiter
from constants import RATE_LIMIT
from utils.exceptions import GroqAPIError, GroqRateLimitError, GroqEmptyResponseError

logger = get_logger(__name__)
router = APIRouter(tags=["Lesson Plans"])

@router.post("/generate-lesson", response_model=APIResponse)
@limiter.limit(RATE_LIMIT)
async def generate_lesson(request: Request, lesson_request: LessonRequest):
    try:
        logger.info(f"Generating lesson for topic: {lesson_request.topic}")
        # Build prompt
        prompt = build_lesson_prompt(lesson_request.topic, lesson_request.grade_level, lesson_request.subject)
        
        # Call groq_service
        content, model_used = groq_service.generate_completion(prompt, LESSON_SYSTEM_PROMPT)
        
        return create_success_response(
            message="Lesson generated successfully",
            data=LessonData(lesson_plan=content),
            model_used=model_used
        )
    except (GroqAPIError, GroqRateLimitError, GroqEmptyResponseError) as e:
        logger.error(f"Groq API error generating lesson: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error generating lesson: {str(e)}")
        raise e
