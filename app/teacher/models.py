from pydantic import BaseModel


class TeacherCreate(BaseModel):
    name: str
    email: str
