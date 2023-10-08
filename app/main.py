from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api_info import description, summary, title, version
from app.auth.router import router as AuthRouter
from app.groups.router import router as TeacherRouter
from app.marks.router import router as MarkRouter
from app.students.router import router as StudentRouter
from app.subject_teacher.router import router as SubjectTeacherRoute
from app.subjects.router import router as SubjectRouter
from app.teacher.router import router as GroupRouter

app = FastAPI(title=title, summary=summary, description=description, version=version)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Welcome to Student Grade System for more info use '/docs'"}


app.include_router(AuthRouter, prefix="/v1")
app.include_router(StudentRouter, prefix="/v1")
app.include_router(TeacherRouter, prefix="/v1")
app.include_router(SubjectRouter, prefix="/v1")
app.include_router(SubjectTeacherRoute, prefix="/v1")
app.include_router(GroupRouter, prefix="/v1")
app.include_router(MarkRouter, prefix="/v1")
