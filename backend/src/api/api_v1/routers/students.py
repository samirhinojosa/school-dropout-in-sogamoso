from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.configs.database import get_db
import src.core.schemas.student as schestu
import src.crud as crud


api_router = APIRouter()


@api_router.get("/", status_code=200, response_model=schestu.StudentId)
async def read_students_id(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)) -> dict:
    """ 
    Fetch all students id
    """

    ids = crud.get_students_id(db, skip=skip, limit=limit)

    return {"ids" : ids}


@api_router.get("/{id}", status_code=200, response_model=schestu.Student)
async def read_student_summary_by_id(id: int, db: Session = Depends(get_db)) -> dict:
    """ 
    Fetch a summary student based on id
    """ 

    student = crud.get_student_summary_by_id(db, id=id)

    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
    
    return student