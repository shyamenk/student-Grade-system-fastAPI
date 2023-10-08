from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext

from app.auth.constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.auth.exceptions import invalid_password, token_decode_error, user_not_found

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
expiry_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


async def authenticate_user(email: str, password: str, db):
    try:
        async with db.cursor() as cursor:
            sql = "SELECT * FROM Users WHERE email = %s"
            await cursor.execute(sql, (email))
            user = await cursor.fetchone()
            if user is None:
                return user_not_found()
            if not verify_password(password, user[3]):
                raise invalid_password()
            return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {e}")


def validate_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return token_decode_error()
    except jwt.DecodeError:
        return token_decode_error()


def create_access_token(email: str, id: int):
    to_encode = {"sub": email, "id": id}
    expire = datetime.utcnow() + expiry_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
