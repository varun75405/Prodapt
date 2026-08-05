from fastapi import APIRouter, Request
from models.requests import LoginRequest
from models.responses import APIResponse, create_success_response, create_error_response, LoginData
from services.auth_service import auth_service
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=APIResponse)
async def login(request: Request, login_request: LoginRequest):
    try:
        logger.info(f"Login attempt for user: {login_request.username}")
        success, message = auth_service.authenticate(login_request.username)
        if success:
            return create_success_response(
                message=message,
                data=LoginData(username=auth_service.get_sanitized_username(login_request.username))
            )
        else:
            return create_error_response(message=message)
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return create_error_response(message="An error occurred during login")
