from typing import List
from dataclasses import fields
from warnings import filters
from sqlalchemy.orm import Session, load_only

from . import models


def get_students_year(db: Session, ANO: int):
    return db.query(models.Students).filter(models.Students.ANO == ANO).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Students).offset(skip).limit(limit).all()

def get_general_statistics(db: Session, fields: List = None, query_filter = None):
    if query_filter:
        query_filter = query_filter
        # query_filter = {
        #     'ANO': 2013,
        #     'ESTRATO': 'ESTRATO 0',
        #     'ESTADO': 1
        # }
    else:
        query_filter = {}
    if fields:
        fields = fields
    else:
        fields = ['ANO', 'ESTRATO', 'ESTADO']

    return db.query(models.Students).options(load_only(*fields)).filter(models.Students.ANO < 2022).filter_by(**query_filter).all()

