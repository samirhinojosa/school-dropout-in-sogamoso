from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Request, Response

from . import crud, models
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

@app.get("/dynamic/", status_code=200)
def read_dynamic_data(field: str, param: str, db: Session = Depends(get_db)):
    data = crud.get_dynamic_data(db, field=field, param=param)
    return data