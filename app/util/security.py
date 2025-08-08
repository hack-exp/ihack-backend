# In app/util/jwt_utils.py

from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.config import settings
from app.util.types import Algorithm

# ... (your existing JWTUtils class) ...


def create_access_token(data: dict) -> str:
    """
    Creates a new JWT access token.

    Args:
        data (dict): The data to be encoded in the token's payload.
        Must contain user identifiers like 'id' and 'sub'.

    Returns:
        str: The encoded JWT as a string.
    """

    # Make a copy of the data to avoid modifying the original dictionary
    to_encode = data.copy()

    # Calculate the expiration time for the token
    # It's best practice to use UTC for server-side timestamps.
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Add the expiration time ('exp') claim to the payload
    # This is a standard JWT claim.
    to_encode.update({"exp": expire})

    # Encode the payload into a JWT using your secret key and algorithm
    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=settings.SECRET_KEY,
        algorithm=Algorithm.HS256.value
    )

    return encoded_jwt