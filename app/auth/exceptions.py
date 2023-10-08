from fastapi import HTTPException, status


def invalid_email_format():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid email format",
    )


def user_not_found():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


def invalid_password():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def expired_token():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )


def token_decode_error():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Error decoding token",
        headers={"WWW-Authenticate": "Bearer"},
    )
