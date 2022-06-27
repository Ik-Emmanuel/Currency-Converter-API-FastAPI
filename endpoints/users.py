from fastapi import APIRouter, HTTPException, Depends, status
from starlette.responses import JSONResponse
from auth.auth import AuthHandler
from db.db import session
from models.user_models import UserInput, User, UserLogin, UserOutput
from datafetch.users_repo import select_all_users, find_user

user_router = APIRouter(
    tags=["User Authentication"],
    prefix="/auth",
)
auth_handler = AuthHandler()


@user_router.post("/registration", status_code=201, description="Register new user")
def register(user: UserInput):
    """
    # Registering a new user
    This requires the following
    - username: str
    - password: str = Field(max_length=256, min_length=6)
    - password2: str
    - email: EmailStr
    """

    users = select_all_users()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail="Username is taken")
    if any(x.email == user.email for x in users):
        raise HTTPException(status_code=400, detail="Email is taken")
    hashed_pwd = auth_handler.get_password_hash(user.password)
    try:
        user = User(username=user.username,
                    password=hashed_pwd, email=user.email)
        session.add(user)
        session.commit()
        registration_response = {
            "status": "Success",
            "message": "User account created successfully",
        }
        return registration_response
    except Exception as e:
        registration_response = {"status": "Error", "message": e}
        return JSONResponse(
            registration_response, status_code=status.HTTP_400_BAD_REQUEST
        )


@user_router.post(
    "/login",
)
def login(user: UserLogin):
    """
    # User Login
    This requires the following
    - email: EmailStr
    - password: str = Field(max_length=256, min_length=6)
    and return an access token
    """
    user_found = find_user(user.username)
    if not user_found:
        raise HTTPException(
            status_code=401, detail="Invalid username and/or password")
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(
            status_code=401, detail="Invalid username and/or password")
    token = auth_handler.encode_token(user_found.username)
    return {"token": token}


@user_router.get("/me", response_model=UserOutput)
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    """
    # Get signed in user using JWT Bearer Token
    """
    return user
