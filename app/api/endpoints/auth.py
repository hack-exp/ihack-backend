# # In your login API endpoint file (e.g., app/api/endpoints/login.py)

# from app.api.deps import GoogleUserDep
# from fastapi import APIRouter, Depends
# from typing import Annotated
# from decouple import config as decouple_conf

# from app.util.google_auth_util import GoogleAuthUtils, GoogleToken
# from app.db.models import User
# # Import your JWT creation function
# from app.util.security import create_access_token # Assuming you have this helper
# from app.api.deps import CurrentUserDep # Your dependency for authenticated users

# router = APIRouter()

# # Create a reusable dependency for getting the user from Google

# @router.post("/login/google")
# async def login_via_google(
#     # This dependency injection handles everything:
#     # 1. Expects a JSON body like {"google_token": "..."}
#     # 2. Verifies the token
#     # 3. Gets or creates the user from the DB
#     # 4. Injects the SQLAlchemy User object into the `google_user` variable
#     google_user: GoogleUserDep,
# ):
#     """
#     Handles Google Sign-In and returns the application's own access token.
#     """
#     print(decouple_conf('DATABASE_NAME'))
#     # The user is already verified and retrieved by the dependency.
#     # Now, just create your application's JWT for that user.
#     access_token = create_access_token(
#         data={"sub": google_user.email, "id": str(google_user.id)}
#     )

#     return {"access_token": access_token, "token_type": "bearer"}


# @router.get("/users/me", response_model=User)
# async def read_users_me(current_user: CurrentUserDep):
#     return current_user