from utils.logger import get_logger

class AuthService:
    """Authentication service abstraction.
    Currently implements demo-only login (any non-empty username succeeds).
    Designed to be replaced with real auth (JWT, OAuth) in production.
    """
    
    def __init__(self):
        self.logger = get_logger(__name__)

    def authenticate(self, username: str) -> tuple[bool, str]:
        """Authenticate a user. Returns (success, message)."""
        # Demo behavior: accept any non-empty username
        if not username or not username.strip():
            self.logger.warning("Authentication failed: empty username")
            return False, "Username cannot be empty"
        sanitized = username.strip()
        if len(sanitized) > 50:
            self.logger.warning("Authentication failed: username too long")
            return False, "Username too long (max 50 characters)"
        
        self.logger.info(f"User authenticated successfully: {sanitized}")
        return True, f"Welcome, {sanitized}!"
    
    def get_sanitized_username(self, username: str) -> str:
        return username.strip()

# Module-level singleton
auth_service = AuthService()
