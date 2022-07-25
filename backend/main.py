import os
import sys
from typing import Optional, List
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import schemas, crud


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
@api_router.get("/api/students/", status_code=200, response_model=schemas.StudentId)
async def read_predicted_students_id(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)) -> dict:
    """ 
    Fetch all students id
    """

    ids = crud.get_predicted_students_id(db, skip=skip, limit=limit)

    return {"ids" : ids}


@api_router.get("/api/students/{id}", status_code=200, response_model=schemas.Student)
async def read_student_details(id: int, db: Session = Depends(get_db)) -> dict:
    """ 
    Fetch a single student by ID
    """ 

    student = crud.get_predicted_student_detail(db, id=id)

    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
    
    return student


@api_router.get("/api/predictions/students/{id}", status_code=200)
async def read_predict(id: int, db: Session = Depends(get_db)) -> dict:
    """ 
    Fetch the probability drop out of a student
    """ 

    student_prediction = crud.get_student_prediction(db, id=id)

    if student_prediction is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
    
    return student_prediction



# @api_router.get("/api/statistics/", status_code=200)
# async def statistics(keyword: Optional[str] = "EDAD") -> dict:
#     """ 
#     Search for statistics based on label keyword
#     """

#     data_not_dropout = df_students_to_predict[df_students_to_predict["ESTADO"]==0].groupby(keyword).size()
#     data_not_dropout = pd.DataFrame(data_not_dropout).reset_index()
#     data_not_dropout.columns = [keyword, "AMOUNT"]
#     data_not_dropout = data_not_dropout.set_index(keyword).to_dict()["AMOUNT"]

#     data_dropout = df_students_to_predict[df_students_to_predict["ESTADO"]==1].groupby(keyword).size()
#     data_dropout = pd.DataFrame(data_dropout).reset_index()
#     data_dropout.columns = [keyword, "AMOUNT"]
#     data_dropout = data_dropout.set_index(keyword).to_dict()["AMOUNT"]

#     return {"not_dropout" : data_not_dropout, "dropout" : data_dropout}
    
























# registering the router
app.include_router(api_router)