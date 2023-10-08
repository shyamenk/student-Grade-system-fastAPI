import re
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class Roles(str, Enum):
    Admin = "admin"
    User = "user"


class UserType(str, Enum):
    Teacher = "teacher"
    Student = "student"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Roles
    user_type: Optional[UserType]

    class Config:
        case_sensitive = False

    @validator("password")
    def password_complexity(cls, v):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$!])[A-Za-z\d@#$!]{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, one special character (@#$!), and one digit."
            )
        return v

    @validator("email")
    def valid_email(cls, v):
        pattern = r"^\S+@\S+\.\S+$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email address.")
        return v


class UserLogin(BaseModel):
    email: str
    password: str


class User(UserCreate):
    id: int


class PasswordChange(BaseModel):
    email: str
    current_password: str
    new_password: str


class EmailData(BaseModel):
    email: str
