from typing import Annotated

from aiomysql import Connection
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependancies import get_current_user
from app.database import get_database_connection
from app.students.utils import is_admin, is_teacher
from app.teacher.models import TeacherCreate
from app.teacher.utils import format_teachers_data

router = APIRouter(prefix="/api/teachers", tags=["Teachers"])

db_dependency = Annotated[Connection, Depends(get_database_connection)]
auth_dependency = Annotated[dict, Depends(get_current_user), db_dependency]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_teachers(db: db_dependency, auth: auth_dependency):
    if not is_admin(auth):
        raise HTTPException(status_code=403, detail="Access forbidden")
    try:
        async with db.cursor() as cursor:
            sql = "SELECT * FROM Teacher"
            await cursor.execute(sql)
            teachers = await cursor.fetchall()
            formatted_students = format_teachers_data(teachers)
            return formatted_students
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving teachers: {e}")


@router.get("/{teacher_id}/students/count", status_code=status.HTTP_200_OK)
async def get_student_count_by_teacher_id(
    teacher_id: int, db: db_dependency, auth: auth_dependency
):
    if not is_admin(auth):
        raise HTTPException(status_code=403, detail="Access forbidden")
    try:
        async with db.cursor() as cursor:
            sql = """
                SELECT COUNT(*) 
                FROM Students 
                WHERE group_id IN (
                    SELECT group_id 
                    FROM Subject_Teacher 
                    WHERE teacher_id = %s
                )
            """
            await cursor.execute(sql, (teacher_id,))
            student_count = await cursor.fetchone()

        return {"student_count": student_count[0]}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving student count: {e}"
        )


@router.get("/{teacher_id}", status_code=status.HTTP_200_OK)
async def get_teacher_by_id(teacher_id: int, db: db_dependency, auth: auth_dependency):
    if not is_admin(auth):
        raise HTTPException(status_code=403, detail="Access forbidden")
    try:
        async with db.cursor() as cursor:
            sql = "SELECT * FROM Teacher WHERE teacher_id = %s"
            await cursor.execute(sql, (teacher_id))
            teacher = await cursor.fetchone()
            if teacher is None:
                raise HTTPException(status_code=404, detail="Teacher not found")
            formatted_student = format_teachers_data([teacher])
            return formatted_student["teachers"][0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving teacher: {e}")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_teacher(teacher: TeacherCreate, db: db_dependency, auth: auth_dependency):
    if not is_admin(auth):
        raise HTTPException(status_code=403, detail="Access forbidden")
    try:
        async with db.cursor() as cursor:
            sql = (
                "INSERT INTO Teacher (name, email, hashed_password) VALUES (%s, %s, %s)"
            )
            await cursor.execute(
                sql, (teacher.name, teacher.email, teacher.hashed_password)
            )
            await db.commit()
            return {"message": "Teacher added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding teacher: {e}")


@router.put("/{teacher_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_teacher(
    teacher_id: int, teacher: TeacherCreate, db: db_dependency, auth: auth_dependency
):
    try:
        if not is_admin(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql = "UPDATE Teacher SET name = %s, email = %s WHERE teacher_id = %s"
            values = (
                teacher.name,
                teacher.email,
                teacher_id,
            )
            await cursor.execute(sql, values)
            await db.commit()
        return {"message": "Teacher updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating teacher: {e}")


@router.delete("/{teacher_id}", status_code=status.HTTP_200_OK)
async def delete_teacher(teacher_id: int, db: db_dependency, auth: auth_dependency):
    try:
        if not is_admin(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql_delete_teacher = "DELETE FROM Teacher WHERE teacher_id = %s"
            await cursor.execute(sql_delete_teacher, (teacher_id,))

            await db.commit()
            return {"message": "Teacher deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting teacher: {e}")
