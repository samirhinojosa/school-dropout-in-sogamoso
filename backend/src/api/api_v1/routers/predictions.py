from typing import Optional
from fastapi import FastAPI, APIRouter, Depends
from src.core.services.student import StudentService


api_router = APIRouter()


@api_router.get("/students/data/{id}", status_code=200)
async def get_student_data_to_predict_by_id(id: int, 
                                            student_service: StudentService = Depends(StudentService)) -> dict:
    """ 
    Fetch data student to predict based on id
    """ 

    return student_service.get_student_data_to_predict_by_id(id)



















