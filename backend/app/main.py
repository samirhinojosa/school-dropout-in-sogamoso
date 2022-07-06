from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Query, HTTPException, Request, Response

from . import crud, models
from .t_response import *
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School dropout Sogamoso - Backend",
    description="""descrpition""",
    version="School dropout Sogamoso - Backend",
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", status_code=200)
def read_root():
    return {"Message": "Request received"}

@app.get("/students/", status_code=200)
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@app.get("/general_statistics/", status_code=200)
def read_general_statistics(db: Session = Depends(get_db), fields: List[str] = Query(None)):
    data = crud.get_general_statistics(db, fields=fields)
    return data

@app.get("/general_statistics_cached/", status_code=200)
def read_general_statistics_cached(fields: List[str] = Query(None)):
    if "ESTRATO" in fields:
        data = info_estrato()
    elif "GENERO" in fields:
        data = info_genero()
    elif "INSTITUCION_ZONA" in fields:
        data = info_zona()
    elif "INSTITUCION_CARACTER" in fields:
        data = info_caracter()
    elif "CATEGORICAL_EDAD" in fields:
        data = info_edad()
    return data


@app.get("/projections/", status_code=200)
def read_projections(db: Session = Depends(get_db), fields: List[str] = Query(None)):
    data = crud.get_projections(db, fields=fields)
    return data