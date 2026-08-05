from fastapi.responses import JSONResponse
from fastapi import Request

class GroqAPIError(Exception):
    pass

class GroqRateLimitError(GroqAPIError):
    pass

class GroqEmptyResponseError(GroqAPIError):
    pass

class ValidationError(Exception):
    pass

def _standard_response(success: bool, message: str, data=None, model_used=None):
    return {
        "success": success,
        "message": message,
        "data": data,
        "model_used": model_used
    }

async def groq_api_error_handler(request: Request, exc: GroqAPIError):
    return JSONResponse(
        status_code=502,
        content=_standard_response(False, str(exc))
    )

async def rate_limit_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=429,
        content=_standard_response(False, "Rate limit exceeded.")
    )

async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content=_standard_response(False, str(exc))
    )

async def generic_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=_standard_response(False, f"Internal Server Error: {str(exc)}")
    )
