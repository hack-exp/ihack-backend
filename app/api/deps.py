from app.db.models import User
from app.util.google_auth_util import GoogleAuthUtils
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from typing import AsyncGenerator
from app.db.session import get_db
from app.db.engine import engine
from app.util.jwt_utils import get_current_user


SessionDep = Annotated[AsyncSession, Depends(get_db)]

GoogleUserDep = Annotated[User, Depends(GoogleAuthUtils.get_user_from_google_token)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]