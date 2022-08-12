from fastapi import APIRouter
from .endpoints import students


api_router = APIRouter()
api_router.include_router(students.api_router, prefix="/students", tags=["students"])