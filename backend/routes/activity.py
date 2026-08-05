from fastapi import APIRouter, Request
from models.requests import ActivityRequest
from models.responses import APIResponse, ActivityData, create_success_response
from services.groq_service import groq_service
from services.prompts import build_activity_prompt, ACTIVITY_SYSTEM_PROMPT
from utils.logger import get_logger
from utils.rate_limiter import limiter
from constants import RATE_LIMIT

logger = get_logger(__name__)
router = APIRouter(tags=["Classroom Activities"])

@router.post("/generate-activity", response_model=APIResponse)
@limiter.limit(RATE_LIMIT)
async def generate_activity(request: Request, activity_request: ActivityRequest):
    try:
        logger.info(f"Generating activity for topic: {activity_request.topic}")
        prompt = build_activity_prompt(activity_request.topic, activity_request.grade_level, activity_request.subject, activity_request.activity_type)
        content, model_used = groq_service.generate_completion(prompt, ACTIVITY_SYSTEM_PROMPT)
        
        return create_success_response(
            message="Activity generated successfully",
            data=ActivityData(activity=content, activity_type=activity_request.activity_type),
            model_used=model_used
        )
    except Exception as e:
        logger.error(f"Error generating activity: {str(e)}")
        raise e
