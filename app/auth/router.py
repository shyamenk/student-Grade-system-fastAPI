from typing import Annotated

from aiomysql import Connection
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependancies import get_current_user
from app.auth.models import UserCreate
from app.auth.utils import authenticate_user, create_access_token, hash_password
from app.database import get_database_connection

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
    responses={401: {"user": "Not authorized"}},
)
db_dependency = Annotated[Connection, Depends(get_database_connection)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/register")
async def register_user(user_data: UserCreate, db: db_dependency):
    try:
        async with db.cursor() as cursor:
            hashed_password = hash_password(user_data.password)
            sql = "INSERT INTO Users (name, email, hashed_password, role, user_type) VALUES (%s, %s, %s, %s, %s)"

            await cursor.execute(
                sql,
                (
                    user_data.name,
                    user_data.email,
                    hashed_password,
                    user_data.role,
                    user_data.user_type or None,
                ),
            )
            await db.commit()
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {e}")


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Connection = Depends(get_database_connection),
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if user:
        access_token = create_access_token(user[2], user[0])
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/profile")
def view_profile(current_user: user_dependency):
    return current_user


# @router.post("/reset_password")
# def send_reset_password_link(email_data: EmailData):
#     return {"message": "Password reset link sent"}


# @router.post("/logout")
# def logout_user(current_user: dict = Depends(get_current_user)):
#     return {"message": "User logged out successfully"}
