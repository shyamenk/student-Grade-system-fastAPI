from typing import Annotated

from aiomysql import Connection
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependancies import get_current_user
from app.database import get_database_connection
from app.groups.models import GroupCreate
from app.groups.utils import format_groups_data
from app.students.utils import is_admin, is_teacher

router = APIRouter(prefix="/api/groups", tags=["Groups"])

db_dependency = Annotated[Connection, Depends(get_database_connection)]
auth_dependency = Annotated[dict, Depends(get_current_user), db_dependency]


@router.get("/")
async def get_all_groups(db: db_dependency, auth: auth_dependency):
    if not is_admin(auth) and not is_teacher(auth):
        raise HTTPException(status_code=403, detail="Access forbidden")

    try:
        async with db.cursor() as cursor:
            sql = "SELECT * FROM Groups"
            await cursor.execute(sql)
            groups = await cursor.fetchall()
            formatted_groups = format_groups_data(groups)
            return formatted_groups
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving groups: {e}")


@router.get("/{group_id}", status_code=status.HTTP_200_OK)
async def get_group_by_id(group_id: int, db: db_dependency, auth: auth_dependency):
    if not is_admin(auth) and not is_teacher(auth):
        raise HTTPException(status_code=403, detail="Access forbidden")

    try:
        async with db.cursor() as cursor:
            sql = "SELECT * FROM Groups WHERE group_id = %s"
            await cursor.execute(sql, (group_id,))
            group = await cursor.fetchone()
            if group is None:
                raise HTTPException(status_code=404, detail="Group not found")
            formatted_group = format_groups_data([group])

            return formatted_group["groups"][0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving group: {e}")


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_group(group: GroupCreate, db: db_dependency, auth: auth_dependency):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql = "INSERT INTO Groups (name) VALUES (%s)"
            await cursor.execute(sql, (group.name,))
            await db.commit()
            return {"message": "Group added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding group: {e}")


@router.put("/update/{group_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_group(
    group: GroupCreate, group_id: int, db: db_dependency, auth: auth_dependency
):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql = "UPDATE Groups SET name = %s WHERE group_id = %s"
            values = (group.name, group_id)
            await cursor.execute(sql, values)
            await db.commit()
        return {"message": "Group updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating group: {e}")


@router.delete("/delete/{group_id}", status_code=status.HTTP_200_OK)
async def delete_group(group_id: int, db: db_dependency, auth: auth_dependency):
    try:
        if not is_admin(auth) and not is_teacher(auth):
            raise HTTPException(status_code=403, detail="Access forbidden")
        async with db.cursor() as cursor:
            sql_delete_group = "DELETE FROM Groups WHERE group_id = %s"
            await cursor.execute(sql_delete_group, (group_id,))
            await db.commit()
            return {"message": "Group deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting group: {e}")
