from pydantic import BaseModel
from typing import Optional, Any, Dict

class APIResponse(BaseModel):
    """Standardized API response wrapper for all endpoints."""
    success: bool
    message: str
    data: Optional[Any] = None
    model_used: Optional[str] = None

class LessonData(BaseModel):
    lesson_plan: str

class QuizData(BaseModel):
    quiz: str

class MaterialData(BaseModel):
    content: str
    material_type: str

class SimplifyData(BaseModel):
    explanations: Dict[str, str]  # keys: elementary, middle, high

class ActivityData(BaseModel):
    activity: str
    activity_type: str

class LoginData(BaseModel):
    username: str

def create_success_response(data: Any, message: str = "Success", model_used: Optional[str] = None) -> APIResponse:
    return APIResponse(
        success=True,
        message=message,
        data=data,
        model_used=model_used
    )

def create_error_response(message: str, model_used: Optional[str] = None) -> APIResponse:
    return APIResponse(
        success=False,
        message=message,
        data=None,
        model_used=model_used
    )
