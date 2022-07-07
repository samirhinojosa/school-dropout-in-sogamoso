from typing import List
from dataclasses import fields
from warnings import filters
from sqlalchemy.orm import Session, load_only

from . import modelos


def get_students_year(db: Session, ANO: int):
    return db.query(modelos.Students).filter(modelos.Students.ANO == ANO).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(modelos.Students).offset(skip).limit(limit).all()

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

    return db.query(modelos.Students).options(load_only(*fields)).filter(modelos.Students.ANO < 2022).filter_by(**query_filter).all()

def get_projections(db: Session, fields: List = None, query_filter = None):
    if fields:
        fields = fields
    else:
        fields = ['ANO', 'ESTRATO', 'ESTADO']

    return db.query(modelos.Pojection).options(load_only(*fields)).filter(modelos.Pojection.ANO == 2022).all()