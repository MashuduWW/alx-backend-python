# messaging_app/chats/auth.py

from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Example custom JWT Authentication class.
    Extend or override methods here if you want to customize token validation.
    """
    pass


# Optional helper function to decode token manually (if needed)
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

def validate_token(token):
    try:
        UntypedToken(token)  # Will raise if invalid
        return True
    except (InvalidToken, TokenError):
        return False
