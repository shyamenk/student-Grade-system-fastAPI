from pydantic import BaseModel


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    group_id: int
