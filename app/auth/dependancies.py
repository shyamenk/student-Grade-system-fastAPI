from typing import Annotated

from aiomysql import Connection
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.auth.constants import ALGORITHM, SECRET_KEY
from app.database import get_database_connection

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

db_dependency = Annotated[Connection, Depends(get_database_connection)]


async def get_current_user(
    token: str = Depends(oauth2_bearer), db: dict = Depends(get_database_connection)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        id: int = payload.get("id")
        async with db.cursor() as cursor:
            sql = "SELECT * FROM Users WHERE id = %s"
            await cursor.execute(sql, id)
            user = await cursor.fetchone()
        if email is None or id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return {"user": user}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication error"
        )
