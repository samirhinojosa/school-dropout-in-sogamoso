from typing import Optional
from fastapi import FastAPI, APIRouter, Depends
from src.core.services.prediction import StudentPredictionService


api_router = APIRouter()


@api_router.get("/students/{id}", status_code=200)
async def get_student_prediction_by_id(id: int, 
                                        student_prediction_service: StudentPredictionService = Depends()) -> dict:
    """ 
    Fetch student prediction based on id
    """ 

    return student_prediction_service.get_student_prediction_by_id(id)