from fastapi import APIRouter
from .routers import students, predictions


api_router = APIRouter()
api_router.include_router(students.api_router, prefix="/students", tags=["students"])
api_router.include_router(predictions.api_router, prefix="/predictions", tags=["predictions"])