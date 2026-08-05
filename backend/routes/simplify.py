from fastapi import APIRouter, Request
import re
from models.requests import SimplifyRequest
from models.responses import APIResponse, SimplifyData, create_success_response
from services.groq_service import groq_service
from services.prompts import build_simplify_prompt, SIMPLIFY_SYSTEM_PROMPT
from utils.logger import get_logger
from utils.rate_limiter import limiter
from constants import RATE_LIMIT

logger = get_logger(__name__)
router = APIRouter(tags=["Topic Simplification"])

def _parse_simplify_response(response_text: str) -> dict:
    """Parse the AI response into three difficulty levels."""
    sections = {
        "elementary": response_text,
        "middle": response_text,
        "high": response_text
    }
    
    try:
        # Regex to match content between headers
        elementary_match = re.search(r'##\s*Elementary School Level\s*(.*?)(?=##\s*Middle School Level|##\s*High School Level|$)', response_text, re.IGNORECASE | re.DOTALL)
        middle_match = re.search(r'##\s*Middle School Level\s*(.*?)(?=##\s*High School Level|$)', response_text, re.IGNORECASE | re.DOTALL)
        high_match = re.search(r'##\s*High School Level\s*(.*?)$', response_text, re.IGNORECASE | re.DOTALL)
        
        if elementary_match and middle_match and high_match:
            sections["elementary"] = elementary_match.group(1).strip()
            sections["middle"] = middle_match.group(1).strip()
            sections["high"] = high_match.group(1).strip()
    except Exception as e:
        logger.error(f"Error parsing simplify response: {str(e)}")
        
    return sections

@router.post("/simplify-concept", response_model=APIResponse)
@limiter.limit(RATE_LIMIT)
async def simplify_concept(request: Request, simplify_request: SimplifyRequest):
    try:
        logger.info(f"Simplifying concept: {simplify_request.concept}")
        prompt = build_simplify_prompt(simplify_request.concept, simplify_request.subject)
        content, model_used = groq_service.generate_completion(prompt, SIMPLIFY_SYSTEM_PROMPT)
        
        parsed_content = _parse_simplify_response(content)
        
        return create_success_response(
            message="Concept simplified successfully",
            data=SimplifyData(explanations=parsed_content),
            model_used=model_used
        )
    except Exception as e:
        logger.error(f"Error simplifying concept: {str(e)}")
        raise e
