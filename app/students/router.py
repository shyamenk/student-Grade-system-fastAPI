from typing import Annotated

from aiomysql import Connection
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependancies import get_current_user
from app.database import get_database_connection
from app.students.models import StudentCreate
from app.students.utils import format_students_data, is_admin, is_teacher

router = APIRouter(prefix="/api/students", tags=["Students"])

db_dependency = Annotated[Connection, Depends(get_database_connection)]
auth_dependency = Annotated[dict, Depends(get_current_user), db_dependency]


@router.get("/")
async def get_all_students(db: db_dependency, auth: auth_dependency):
    if not is_admin(auth) and not is_teacher(auth):
        raise HTTPException(status_code=403, detail="Access forbidden")

    try:
        async with db.cursor() as cursor:
            sql = "SELECT * FROM Students"
            await cursor.execute(sql)
            students = await cursor.fetchall()
            formatted_students = format_students_data(students)
            return formatted_students
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving students: {e}")


@router.get("/{student_id}", status_code=status.HTTP_200_OK)
async def get_student_by_id(student_id: int, db: db_dependency):
    try:
        async with db.cursor() as cursor:
            sql = "SELECT * FROM Students WHERE student_id = %s"
            await cursor.execute(sql, (student_id,))
            student = await cursor.fetchone()
            if student is None:
                raise HTTPException(status_code=404, detail="Student not found")
            formatted_student = format_students_data([student])
            return formatted_student["students"][0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving student: {e}")


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_student(student: StudentCreate, db: db_dependency, auth: auth_dependency):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql = "INSERT INTO Students (first_name, last_name, group_id) VALUES (%s, %s, %s)"
            await cursor.execute(
                sql, (student.first_name, student.last_name, student.group_id)
            )
            await db.commit()
            return {"message": "Student added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding student: {e}")


@router.put("/update/{student_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_student(
    student: StudentCreate, student_id: int, db: db_dependency, auth: auth_dependency
):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql = "UPDATE Students SET first_name = %s, last_name = %s, group_id = %s WHERE student_id = %s"
            values = (
                student.first_name,
                student.last_name,
                student.group_id,
                student_id,
            )
            await cursor.execute(sql, values)
            await db.commit()
        return {"message": "Student updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating student: {e}")


@router.delete("/delete/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student(student_id: int, db: db_dependency, auth: auth_dependency):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql_delete_marks = "DELETE FROM Marks WHERE student_id = %s"
            await cursor.execute(sql_delete_marks, (student_id,))

            sql_delete_student = "DELETE FROM Students WHERE student_id = %s"
            await cursor.execute(sql_delete_student, (student_id,))

            await db.commit()
            return {"message": "Student deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting student: {e}")
