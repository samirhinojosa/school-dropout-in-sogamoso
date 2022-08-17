from fastapi import APIRouter
from .routers import student, prediction, statistic


api_router = APIRouter()
api_router.include_router(student.api_router, prefix="/students", tags=["Students"])
api_router.include_router(prediction.api_router, prefix="/predictions", tags=["Predictions"])
api_router.include_router(statistic.api_router, prefix="/statistics", tags=["Statistics"])