from fastapi import APIRouter, Request
from models.requests import MaterialRequest
from models.responses import APIResponse, MaterialData, create_success_response
from services.groq_service import groq_service
from services.prompts import build_material_prompt, MATERIAL_SYSTEM_PROMPT
from utils.logger import get_logger
from utils.rate_limiter import limiter
from constants import RATE_LIMIT

logger = get_logger(__name__)
router = APIRouter(tags=["Learning Materials"])

@router.post("/generate-material", response_model=APIResponse)
@limiter.limit(RATE_LIMIT)
async def generate_material(request: Request, material_request: MaterialRequest):
    try:
        logger.info(f"Generating material for topic: {material_request.topic}")
        prompt = build_material_prompt(material_request.topic, material_request.grade_level, material_request.subject, material_request.material_type)
        content, model_used = groq_service.generate_completion(prompt, MATERIAL_SYSTEM_PROMPT)
        
        return create_success_response(
            message="Material generated successfully",
            data=MaterialData(content=content, material_type=material_request.material_type),
            model_used=model_used
        )
    except Exception as e:
        logger.error(f"Error generating material: {str(e)}")
        raise e
