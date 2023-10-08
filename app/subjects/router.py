from typing import Annotated

from aiomysql import Connection
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependancies import get_current_user
from app.database import get_database_connection
from app.students.utils import is_admin, is_teacher
from app.subjects.models import SubjectCreate
from app.subjects.utils import format_subjects_data

router = APIRouter(prefix="/api/subjects", tags=["Subjects"])

db_dependency = Annotated[Connection, Depends(get_database_connection)]
auth_dependency = Annotated[dict, Depends(get_current_user), db_dependency]


@router.get("/")
async def get_all_subjects(db: db_dependency, auth: auth_dependency):
    if not is_admin(auth) and not is_teacher(auth):
        raise HTTPException(status_code=403, detail="Access forbidden")

    try:
        async with db.cursor() as cursor:
            sql = "SELECT * FROM Subjects"
            await cursor.execute(sql)
            subjects = await cursor.fetchall()
            formatted_subjects = format_subjects_data(subjects)
            return formatted_subjects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving subjects: {e}")


@router.get("/{subject_id}", status_code=status.HTTP_200_OK)
async def get_subject_by_id(subject_id: int, db: db_dependency, auth: auth_dependency):
    if not is_admin(auth) and not is_teacher(auth):
        raise HTTPException(status_code=403, detail="Access forbidden")

    try:
        async with db.cursor() as cursor:
            sql = "SELECT * FROM Subjects WHERE subject_id = %s"
            await cursor.execute(sql, (subject_id,))
            subject = await cursor.fetchone()
            if subject is None:
                raise HTTPException(status_code=404, detail="Subject not found")
            formatted_subject = format_subjects_data([subject])
            print(formatted_subject)

            return formatted_subject["subjects"][0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving subject: {e}")


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_subject(subject: SubjectCreate, db: db_dependency, auth: auth_dependency):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql = "INSERT INTO Subjects (title) VALUES (%s)"
            await cursor.execute(sql, (subject.title,))
            await db.commit()
            return {"message": "Subject added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding subject: {e}")


@router.put("/update/{subject_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_subject(
    subject: SubjectCreate, subject_id: int, db: db_dependency, auth: auth_dependency
):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql = "UPDATE Subjects SET title = %s WHERE subject_id = %s"
            values = (subject.title, subject_id)
            await cursor.execute(sql, values)
            await db.commit()
        return {"message": "Subject updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating subject: {e}")


@router.delete("/delete/{subject_id}", status_code=status.HTTP_200_OK)
async def delete_subject(subject_id: int, db: db_dependency, auth: auth_dependency):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql_delete_subject = "DELETE FROM Subjects WHERE subject_id = %s"
            await cursor.execute(sql_delete_subject, (subject_id,))
            await db.commit()
            return {"message": "Subject deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting subject: {e}")
