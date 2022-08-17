from typing import Optional
from fastapi import FastAPI, APIRouter, Depends
import src.core.schemas.student as schestu
from src.core.services.student import StudentService


api_router = APIRouter()


@api_router.get("", status_code=200, response_model=schestu.StudentId)
async def read_students_id(skip: Optional[int] = 0, limit: Optional[int] = 1000,
                            student_service: StudentService = Depends()):
    """ 
    Fetch all students id
    """  
    return student_service.get_students_id(skip, limit)


@api_router.get("/{id}", status_code=200, response_model=schestu.Student)
async def read_student_summary_by_id(id: int,
                                        student_service: StudentService = Depends(StudentService)) -> dict:
    """ 
    Fetch a summary student based on id
    """ 
    return student_service.get_student_summary_by_id(id)