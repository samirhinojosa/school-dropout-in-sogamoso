from sqlalchemy.orm import Session

from . import models


def get_students_year(db: Session, ANO: int):
    return db.query(models.Students).filter(models.Students.ANO == ANO).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Students).offset(skip).limit(limit).all()

