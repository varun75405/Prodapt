import groq
from config import GROQ_API_KEY
from constants import PRIMARY_MODEL, FALLBACK_MODEL, GROQ_TIMEOUT, GROQ_MAX_TOKENS, GROQ_TEMPERATURE
from utils.logger import get_logger
from utils.exceptions import GroqAPIError, GroqRateLimitError, GroqEmptyResponseError

class GroqService:
    def __init__(self):
        self.client = groq.Groq(api_key=GROQ_API_KEY)
        self.logger = get_logger(__name__)
        self.primary_model = PRIMARY_MODEL
        self.fallback_model = FALLBACK_MODEL

    def generate_completion(self, prompt: str, system_message: str) -> tuple[str, str]:
        """Generate a completion using Groq API with automatic fallback.
        Returns (generated_text, model_name_used).
        Tries primary model first, falls back to secondary on rate limit."""
        
        # Try primary model
        try:
            response = self._call_model(self.primary_model, prompt, system_message)
            return response, self.primary_model
        except groq.RateLimitError as e:
            self.logger.warning(f"Primary model rate limited: {e}. Falling back to {self.fallback_model}")
        except groq.APIError as e:
            self.logger.warning(f"Primary model API error: {e}. Falling back to {self.fallback_model}")
        
        # Try fallback model
        try:
            response = self._call_model(self.fallback_model, prompt, system_message)
            return response, self.fallback_model
        except groq.RateLimitError as e:
            self.logger.error(f"Fallback model also rate limited: {e}")
            raise GroqRateLimitError(f"Both models are rate limited. Please try again later.")
        except groq.APIError as e:
            self.logger.error(f"Fallback model API error: {e}")
            raise GroqAPIError(f"AI service is temporarily unavailable. Please try again later.")

    def _call_model(self, model: str, prompt: str, system_message: str) -> str:
        """Make a single API call to the specified model."""
        self.logger.info(f"Calling Groq API with model: {model}")
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            max_tokens=GROQ_MAX_TOKENS,
            temperature=GROQ_TEMPERATURE,
            timeout=GROQ_TIMEOUT
        )
        
        # Validate response
        content = self._validate_response(response)
        return content

    def _validate_response(self, response) -> str:
        """Validate that the Groq response contains usable content."""
        if not response or not response.choices:
            raise GroqEmptyResponseError("Received empty response from AI model.")
        
        content = response.choices[0].message.content
        if not content or not content.strip():
            raise GroqEmptyResponseError("AI model returned empty content. Please try again.")
        
        return content.strip()

# Module-level singleton
groq_service = GroqService()
