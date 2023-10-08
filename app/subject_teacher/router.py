from typing import Annotated

from aiomysql import Connection
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependancies import get_current_user
from app.database import get_database_connection
from app.students.utils import is_admin, is_teacher

router = APIRouter(prefix="/api/subject_teacher", tags=["Subject Teacher"])

db_dependency = Annotated[Connection, Depends(get_database_connection)]
auth_dependency = Annotated[dict, Depends(get_current_user), db_dependency]


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_subject_to_teacher(
    subject_id: int,
    teacher_id: int,
    group_id: int,
    db: db_dependency,
    auth: auth_dependency,
):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql = "INSERT INTO Subject_Teacher (subject_id, teacher_id, group_id) VALUES (%s, %s, %s)"
            await cursor.execute(sql, (subject_id, teacher_id, group_id))
            await db.commit()
            return {"message": "Subject Teacher relationship added successfully!"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error adding Subject Teacher relationship: {e}"
        )


@router.delete("/delete/{subject_id}/{teacher_id}", status_code=status.HTTP_200_OK)
async def delete_subject_from_teacher(
    subject_id: int, teacher_id: int, db: db_dependency, auth: auth_dependency
):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql = (
                "DELETE FROM Subject_Teacher WHERE subject_id = %s AND teacher_id = %s"
            )
            await cursor.execute(sql, (subject_id, teacher_id))
            await db.commit()
            return {"message": "Subject Teacher relationship deleted successfully!"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting Subject Teacher relationship: {e}"
        )


router_marks = APIRouter(prefix="/api/marks", tags=["Marks"])
