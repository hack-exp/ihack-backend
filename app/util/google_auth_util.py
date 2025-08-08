from fastapi import Depends, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
from pydantic import BaseModel
from app.db.models import User
from sqlalchemy import select
from app.core.config import settings
from app.db.session import SessionDep

class GoogleToken(BaseModel):
    google_token: str


class GoogleAuthUtils:
    """
    Utility class for handling Google OAuth2 authentication.
    """

    @staticmethod
    async def get_user_from_google_token(
        token_data: GoogleToken, db: SessionDep
    ) -> User:
        """
        Verifies a Google ID token, then finds or creates a user in the database.

        Args:
            token_data (GoogleToken): The Pydantic model containing the Google token.
            db (SessionDep): The database session dependency.

        Returns:
            User: The SQLAlchemy User object corresponding to the token.

        Raises:
            HTTPException: If the token is invalid or verification fails.
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                token_data.google_token, requests.Request(), settings.GOOGLE_CLIENT_ID
            )
            user_email = idinfo.get("email")

            if not user_email:
                raise HTTPException(
                    status_code=400, detail="Email not found in Google token."
                )

        except ValueError as e:
            raise HTTPException(status_code=401, detail=f"Invalid Google token: {e}")

        
        result = await db.execute(select(User).where(User.email == user_email))
        user = result.scalars().first()
        if not user:
            user_name = idinfo.get("name")
            picture_url = idinfo.get("picture") 
            new_user = User(
                email=user_email,
                name=user_name,
                picture_url=picture_url, 
            )
            user = new_user
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user
