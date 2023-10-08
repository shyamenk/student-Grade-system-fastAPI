from pydantic import BaseModel


class SubjectCreate(BaseModel):
    title: str
