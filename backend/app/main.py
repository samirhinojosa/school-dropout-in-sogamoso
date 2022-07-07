import os
import joblib
import numpy as np
import pandas as pd
from xgboost import XGBClassifier

from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Query, HTTPException, Request, Response, File

from . import crud, models
from .t_response import *
from .database import SessionLocal, engine
from .custom_transformer import *

# try:
#     from modx import does_something
#     from custom_transformer import *
# except ImportError:
#     from .custom_transformer import *
    # from .modx import does_something

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School dropout Sogamoso - Backend",
    description="""descrpition""",
    version="1.0.0",
)

# def boolean_transformation(X):
#     return X.astype(int)

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

@app.get("/students_paginated/", status_code=200)
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


########################################################
# Reading the csv
########################################################
# df_students_to_predict = pd.read_csv("datasets/df_students_2022_predicted.csv")
df_students_to_predict = pd.read_csv(os.path.join(os.path.dirname(__file__), "datasets/df_students_2022_predicted.csv"))


########################################################
# Columns to read on CSVs
########################################################
COLUMNS_DETAILS = [
    "PER_ID", "EDAD", "GENERO", "INSTITUCION",
    "GRADO_COD", "JORNADA", "ESTRATO",
    "DISCAPACIDAD", "PAIS_ORIGEN"
]

COLUMNS_COMPLETE = [
    "INSTITUCION", "GENERO", "JORNADA", "PAIS_ORIGEN", "DISCAPACIDAD",
    "SRPA", "INSTITUCION_SECTOR", "INSTITUCION_MODELO", 
    "INSTITUCION_APOYO_ACADEMICO_ESPECIAL", "INSTITUCION_ZONA",
    "INSTITUCION_CARACTER", "INSTITUCION_ESTADO", 
    "INSTITUCION_PRESTADOR_DE_SERVICIO", "EDAD_CLASIFICACION", 
    "GRADO_COD", "ESTRATO", "INSTITUCION_TAMAÑO",
    "INSTITUCION_NUMERO_DE_SEDES", "INSTITUCION_NIVEL_BASICA_PRIMARIA", 
    "INSTITUCION_NIVEL_SECUNDARIA_PRIMARIA", "INSTITUCION_NIVEL_MEDIA",
    "INSTITUCION_NIVEL_PREESCOLAR", "INSTITUCION_NIVEL_PRIMERA_INFANCIA", 
    "INSTITUCION_ESPECIALIDAD_ACADÉMICA", "INSTITUCION_ESPECIALIDAD_AGROPECUARIO",
    "INSTITUCION_ESPECIALIDAD_COMERCIAL", "INSTITUCION_ESPECIALIDAD_INDUSTRIAL",
    "INSTITUCION_ESPECIALIDAD_NO_APLICA", "INSTITUCION_ESPECIALIDAD_OTRO"
]

########################################################
# EndPoints
########################################################
@app.get("/api/students")
async def students_id():
    """ 
    EndPoint to get all students id
    """
    
    students_id = df_students_to_predict["PER_ID"].tolist()

    return {"StudentsId": students_id}


@app.get("/api/students/{id}")
async def student_details(id: int):
    """ 
    EndPoint to get student's detail 
    """ 

    students_id = df_students_to_predict["PER_ID"].tolist()

    if id not in students_id:
        raise HTTPException(status_code=404, detail="student's id not found")
    else:
        # Filtering by student's id
        student_id = df_students_to_predict[COLUMNS_DETAILS][df_students_to_predict["PER_ID"] == id]
        idx = df_students_to_predict[df_students_to_predict["PER_ID"]==id].index[0]

        for col in student_id.columns:
            globals()[col] = student_id.iloc[0, student_id.columns.get_loc(col)]
        
        student = {
            "studentId" : int(PER_ID),
            "gender" : GENERO,
            "age" : int(EDAD),
            "institution" : INSTITUCION,
            "schoolGrade" : int(GRADO_COD),
            "schoolDay" : JORNADA,
            "stratum" : ESTRATO,
            "disability" : DISCAPACIDAD,
            "countryOrigin" : PAIS_ORIGEN,
            "shapPosition" : int(idx)
        }

    return student


@app.get("/api/predictions/students/{id}")
async def predict(id: int):
    """ 
    EndPoint to get the probability drop out of a student
    """ 

    students_id = df_students_to_predict["PER_ID"].tolist()

    if id not in students_id:
        raise HTTPException(status_code=404, detail="client's id not found")
    else:
        # Loading the model
        # df_students_to_predict = pd.read_csv(os.path.join(os.path.dirname(__file__), "datasets/df_students_2022_predicted.csv"))
        # model = joblib.load("models/model_20220706.pkl")
        # model = joblib.load("/Users/tavo/Documents/Study/DS4A2022/school-dropout-in-sogamoso/backend/app/models/model_20220706.pkl")
        # location = 'models/'
        fullpath = os.path.join(os.path.dirname(__file__), 'models/model_20220706.pkl')
        model = joblib.load(fullpath)
        # model = joblib.load(os.path.dirname(__file__), "models/model_20220706.pkl")

        threshold = 0.632

        # Filtering by client's id
        df_prediction_by_id = df_students_to_predict[df_students_to_predict["PER_ID"] == id]
        df_prediction_by_id = df_prediction_by_id.loc[:, COLUMNS_COMPLETE]

        # Predicting
        result_proba = model.predict_proba(df_prediction_by_id)
        y_prob = result_proba[:, 1]

        result = (y_prob >= threshold).astype(int)

        if (int(result[0]) == 0):
            result = "Yes"
        else:
            result = "No"    

    return {
        "dropOut" : result,
        "probability" : result_proba[0].tolist(),
        "threshold" : threshold
    }


@app.get("/api/predictions/shap/students/{id}")
async def predict(id: int):
    """ 
    EndPoint to get the student data to plot the local interpretation with SHAP
    """ 

    students_id = df_students_to_predict["PER_ID"].tolist()

    if id not in students_id:
        raise HTTPException(status_code=404, detail="client's id not found")
    else:

        # Filtering by client's id
        df_prediction_by_id = df_students_to_predict[df_students_to_predict["PER_ID"] == id]
        student = df_prediction_by_id[COLUMNS_COMPLETE].copy()
        student = student.to_json(orient="records")

    return student


@app.get("/api/statistics/ages")
async def statistical_age():
    """ 
    EndPoint to get some statistics - ages
    """

    ages_data_not_dropout = df_students_to_predict[df_students_to_predict["ESTADO"]==0].groupby("EDAD").size()
    ages_data_not_dropout = pd.DataFrame(ages_data_not_dropout).reset_index()
    ages_data_not_dropout.columns = ["EDAD", "AMOUNT"]
    ages_data_not_dropout = ages_data_not_dropout.set_index("EDAD").to_dict()["AMOUNT"]

    ages_data_dropout = df_students_to_predict[df_students_to_predict["ESTADO"]==1].groupby("EDAD").size()
    ages_data_dropout = pd.DataFrame(ages_data_dropout).reset_index()
    ages_data_dropout.columns = ["EDAD", "AMOUNT"]
    ages_data_dropout = ages_data_dropout.set_index("EDAD").to_dict()["AMOUNT"]

    return {"ages_not_dropout" : ages_data_not_dropout, "ages_dropout" : ages_data_dropout}


@app.get("/api/statistics/stratums")
async def statistical_stratums():
    """ 
    EndPoint to get some statistics - stratums
    """

    stratum_data_not_dropout = df_students_to_predict[df_students_to_predict["ESTADO"]==0].groupby("ESTRATO").size()
    stratum_data_not_dropout = pd.DataFrame(stratum_data_not_dropout).reset_index()
    stratum_data_not_dropout.columns = ["ESTRATO", "AMOUNT"]
    stratum_data_not_dropout = stratum_data_not_dropout.set_index("ESTRATO").to_dict()["AMOUNT"]
    stratum_data_not_dropout = {int(k.replace("ESTRATO ", "")) : v for k, v in stratum_data_not_dropout.items()}

    stratum_data_dropout = df_students_to_predict[df_students_to_predict["ESTADO"]==1].groupby("ESTRATO").size()
    stratum_data_dropout = pd.DataFrame(stratum_data_dropout).reset_index()
    stratum_data_dropout.columns = ["ESTRATO", "AMOUNT"]
    stratum_data_dropout = stratum_data_dropout.set_index("ESTRATO").to_dict()["AMOUNT"]
    stratum_data_dropout = {int(k.replace("ESTRATO ", "")) : v for k, v in stratum_data_dropout.items()}

    return {"stratum_not_dropout" : stratum_data_not_dropout, "stratum_dropout" : stratum_data_dropout}
