from typing import Annotated

from aiomysql import Connection
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependancies import get_current_user
from app.database import get_database_connection
from app.students.utils import is_admin, is_teacher

router = APIRouter(prefix="/api/marks", tags=["Student Marks"])

db_dependency = Annotated[Connection, Depends(get_database_connection)]
auth_dependency = Annotated[dict, Depends(get_current_user), db_dependency]


@router.get("/{student_id}", status_code=status.HTTP_200_OK)
async def get_marks_by_student_id(student_id: int, db: db_dependency):
    try:
        async with db.cursor() as cursor:
            sql = "SELECT mark FROM Marks WHERE student_id = %s"
            await cursor.execute(sql, (student_id,))
            marks = await cursor.fetchall()

        return {"marks": marks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving marks: {e}")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_marks_by_student_id(student_id: int, db: db_dependency):
    try:
        async with db.cursor() as cursor:
            sql = """
                SELECT m.mark, s.title
                FROM Marks m
                JOIN Subjects s ON m.subject_id = s.subject_id
                JOIN Students st ON m.student_id = st.student_id
                WHERE m.student_id = %s
            """
            await cursor.execute(sql, (student_id,))
            marks = await cursor.fetchall()

        return {"marks": marks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving marks: {e}")


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_mark(
    student_id: int,
    subject_id: int,
    date: str,
    mark: int,
    db: db_dependency,
    auth: auth_dependency,
):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql = "INSERT INTO Marks (student_id, subject_id, date, mark) VALUES (%s, %s, %s, %s)"
            await cursor.execute(sql, (student_id, subject_id, date, mark))
            await db.commit()
            return {"message": "Mark added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding mark: {e}")


@router.put("/update/{mark_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_mark(
    mark_id: int,
    student_id: int,
    subject_id: int,
    date: str,
    mark: int,
    db: db_dependency,
    auth: auth_dependency,
):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql = "UPDATE Marks SET student_id = %s, subject_id = %s, date = %s, mark = %s WHERE mark_id = %s"
            values = (student_id, subject_id, date, mark, mark_id)
            await cursor.execute(sql, values)
            await db.commit()
            return {"message": "Mark updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating mark: {e}")


@router.delete("/delete/{mark_id}", status_code=status.HTTP_200_OK)
async def delete_mark(mark_id: int, db: db_dependency, auth: auth_dependency):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql = "DELETE FROM Marks WHERE mark_id = %s"
            await cursor.execute(sql, (mark_id,))
            await db.commit()
            return {"message": "Mark deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting mark: {e}")
