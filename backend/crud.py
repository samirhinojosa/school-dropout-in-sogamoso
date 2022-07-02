from dataclasses import fields
from sqlalchemy.orm import Session, load_only

from . import models


def get_students_year(db: Session, ANO: int):
    return db.query(models.Students).filter(models.Students.ANO == ANO).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Students).offset(skip).limit(limit).all()

def get_dynamic_data(db: Session, field: str, param: str):
    if field == 'ESTRATO':
        filter = (models.Students.ESTRATO == param)
    filter_test = {
        'ANO': 2013,
        'ESTRATO': 'ESTRATO 0',
        'ESTADO': 1
    }
    fields = ['ANO', 'ESTRATO', 'ESTADO']
    return db.query(models.Students).options(load_only(*fields)).filter_by(**filter_test).all()
    # return db.query(models.Students).with_entities(models.Students.ANO).filter_by(**filter_test).all()
    # return db.query(models.Students).filter(*filter).all()

