import os
import sys
from typing import Optional, List
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from settings.database import SessionLocal, engine
import core.schemas.student as schestu
import crud


app = FastAPI(
    title="School dropout Sogamoso - Backend",
    description="""descrpition""",
    version="1.0.0",
    openapi_url="/openapi.json"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


api_router = APIRouter()


########################################################
# EndPoints
########################################################
@api_router.get("/api/students/", status_code=200, response_model=schestu.StudentId)
async def read_students_id_to_predict(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)) -> dict:
    """ 
    Fetch all students id
    """

    ids = crud.get_students_id_to_predict(db, skip=skip, limit=limit)

    return {"ids" : ids}


@api_router.get("/api/students/{id}", status_code=200, response_model=schestu.Student)
async def read_summary_student_detail_by_id(id: int, db: Session = Depends(get_db)) -> dict:
    """ 
    Fetch a summary student based on id
    """ 

    student = crud.get_summary_student_detail_by_id(db, id=id)

    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
    
    return student


@api_router.get("/api/predictions/students/{id}", status_code=200)
async def read_student_prediction(id: int, db: Session = Depends(get_db)) -> dict:
    """ 
    Fetch the probability drop out of a student
    """ 

    student_prediction = crud.get_student_prediction(db, id=id)

    if student_prediction is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
    
    return student_prediction


#@app.get("/api/predictions/shap/students/{id}", status_code=200)
#async def read_student_by_id(id: int, db: Session = Depends(get_db)) -> dict:
#    """ 
#    Fetch student data based on id, to plot the local interpretation with SHAP
#    """ 
#
#    student = crud.get_student_by_id(db, id=id)
#
#   if student is None:
#        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
#    
#    return student


@api_router.get("/api/statistics/age/", status_code=200)
async def read_statistics_age(db: Session = Depends(get_db)) -> dict:
    """ 
    Fetch student statistics by age XXXX
    """ 

    statistics = crud.get_statistics_age(db)

    if statistics is None:
        raise HTTPException(status_code=404, detail=f"Statistics age not found")

    return {"ages_not_dropout" : statistics[0], "ages_dropout" : statistics[1]}


@api_router.get("/api/statistics/stratum/", status_code=200)
async def read_statistics_stratum(db: Session = Depends(get_db)) -> dict:
    """ 
    Fetch student statistics by stratum
    """ 

    statistics = crud.get_statistics_stratum(db)

    if statistics is None:
        raise HTTPException(status_code=404, detail=f"Statistics stratum not found")

    return {"stratums_not_dropout" : statistics[0], "stratums_dropout" : statistics[1]}


@api_router.get("/api/statistics/general/", status_code=200)
def read_statistics_general(db: Session = Depends(get_db), fields: List[str] = Query(None)):
    data = crud.get_statistics_general(db, fields=fields)
    return data


# registering the router
app.include_router(api_router)
