from typing import Optional
from fastapi import FastAPI, APIRouter, Depends
from src.core.services.student import StudentService


api_router = APIRouter()


@api_router.get("/age", status_code=200)
async def read_statistics_age(student_service: StudentService = Depends(StudentService)) -> dict:
    """ 
    Fetch student statistics by age
    """ 
    return student_service.get_statistics_age()


@api_router.get("/stratum", status_code=200)
async def read_statistics_stratum(student_service: StudentService = Depends(StudentService)) -> dict:
    """ 
    Fetch student statistics by stratum
    """ 
    return student_service.get_statistics_stratum()