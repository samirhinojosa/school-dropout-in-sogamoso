from typing import Optional, List
from sqlalchemy.orm import Session, load_only
from sqlalchemy import func, asc
import pandas as pd
import joblib
import models
from custom_transformer import *


def get_students_id_to_predict(db: Session, skip: int = 0, limit: int = 1000):
    """ 
    Fetch all students id
    """ 
    result =  db.query(models.PredictedStudent)\
                .with_entities(models.PredictedStudent.per_id)\
                .offset(skip).limit(limit).all()

    STUDENTS_ID = [id[0] for id in result]

    return STUDENTS_ID


def get_summary_student_detail_by_id(db: Session, id: int):
    """ 
    Fetch a single student by ID
    """ 

    result = db.query(models.PredictedStudent)\
                .with_entities(
                    models.PredictedStudent.per_id, models.PredictedStudent.genero,
                    models.PredictedStudent.edad, models.PredictedStudent.institucion,
                    models.PredictedStudent.grado_cod, models.PredictedStudent.jornada,
                    models.PredictedStudent.estrato, models.PredictedStudent.discapacidad,
                    models.PredictedStudent.pais_origen, models.PredictedStudent.idx
                )\
                .filter(models.PredictedStudent.per_id == id).first()
    
    student = {
            "id" : result[0],
            "gender" : result[1],
            "age" : result[2],
            "institution" : result[3],
            "schoolGrade" : result[4],
            "schoolDay" : result[5],
            "stratum" : result[6],
            "disability" : result[7],
            "countryOrigin" : result[8],
            "shapPosition" : result[9]
        }

    return student


def get_student_by_id(db: Session, id: int):
    """ 
    Fetch student data based on id
    """ 

    result = db.query(models.PredictedStudent)\
                .with_entities(
                    models.PredictedStudent.institucion, models.PredictedStudent.genero,
                    models.PredictedStudent.jornada, models.PredictedStudent.pais_origen,
                    models.PredictedStudent.discapacidad, models.PredictedStudent.srpa,
                    models.PredictedStudent.institucion_sector, models.PredictedStudent.institucion_modelo,
                    models.PredictedStudent.institucion_apoyo_academico_especial, 
                    models.PredictedStudent.institucion_zona, models.PredictedStudent.institucion_caracter,
                    models.PredictedStudent.institucion_estado, 
                    models.PredictedStudent.institucion_prestador_de_servicio,
                    models.PredictedStudent.edad_clasificacion, models.PredictedStudent.grado_cod,
                    models.PredictedStudent.estrato, models.PredictedStudent.institucion_tamanyo,
                    models.PredictedStudent.institucion_numero_de_sedes, 
                    models.PredictedStudent.institucion_nivel_basica_primaria,
                    models.PredictedStudent.institucion_nivel_secundaria_primaria,
                    models.PredictedStudent.institucion_nivel_media, 
                    models.PredictedStudent.institucion_nivel_preescolar,
                    models.PredictedStudent.institucion_nivel_primera_infancia,
                    models.PredictedStudent.institucion_especialidad_academica,
                    models.PredictedStudent.institucion_especialidad_agropecuario,
                    models.PredictedStudent.institucion_especialidad_comercial,
                    models.PredictedStudent.institucion_especialidad_industrial,
                    models.PredictedStudent.institucion_especialidad_no_aplica,
                    models.PredictedStudent.institucion_especialidad_otro,
                    models.PredictedStudent.idx
                )\
                .filter(models.PredictedStudent.per_id == id).first()

    if result is None:

        return result

    else:

        threshold = 0.632

        student = {
                "INSTITUCION" : result[0],
                "GENERO" : result[1],
                "JORNADA" : result[2],
                "PAIS_ORIGEN" : result[3],
                "DISCAPACIDAD" : result[4],
                "SRPA" : result[5],
                "INSTITUCION_SECTOR" : result[6],
                "INSTITUCION_MODELO" : result[7],
                "INSTITUCION_APOYO_ACADEMICO_ESPECIAL" : result[8],
                "INSTITUCION_ZONA" : result[9],
                "INSTITUCION_CARACTER" : result[10],
                "INSTITUCION_ESTADO" : result[11],
                "INSTITUCION_PRESTADOR_DE_SERVICIO" : result[12],
                "EDAD_CLASIFICACION" : result[13],
                "GRADO_COD" : result[14],
                "ESTRATO" : result[15],
                "INSTITUCION_TAMAÑO" : result[16],
                "INSTITUCION_NUMERO_DE_SEDES" : result[17],
                "INSTITUCION_NIVEL_BASICA_PRIMARIA" : result[18],
                "INSTITUCION_NIVEL_SECUNDARIA_PRIMARIA" : result[19],
                "INSTITUCION_NIVEL_MEDIA" : result[20],
                "INSTITUCION_NIVEL_PREESCOLAR" : result[21],
                "INSTITUCION_NIVEL_PRIMERA_INFANCIA" : result[22],
                "INSTITUCION_ESPECIALIDAD_ACADÉMICA" : result[23],
                "INSTITUCION_ESPECIALIDAD_AGROPECUARIO" : result[24],
                "INSTITUCION_ESPECIALIDAD_COMERCIAL" : result[25],
                "INSTITUCION_ESPECIALIDAD_INDUSTRIAL" : result[26],
                "INSTITUCION_ESPECIALIDAD_NO_APLICA" : result[27],
                "INSTITUCION_ESPECIALIDAD_OTRO" : result[28]
            }

        return student


def get_student_prediction(db: Session, id: int):
    """ 
    Fetch student prediction
    """ 

    student = get_student_by_id(db, id)

    if student is None:

        return student

    else:

        threshold = 0.632

        # Loading the model
        model = joblib.load("pickles/model_20220706.pkl")

        # Predicting
        result_proba = model.predict_proba(pd.DataFrame([student]))
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


def get_statistics_age(db: Session):
    """ 
    Fetch student statistics by age
    """ 

    not_dropout = db.query(models.PredictedStudent.edad, 
                    func.count(models.PredictedStudent.edad).label("AMOUNT")
                )\
                .filter(models.PredictedStudent.estado == 0)\
                .group_by(models.PredictedStudent.edad)\
                .order_by(models.PredictedStudent.edad.asc())\
                .all()
            
    dropout = db.query(models.PredictedStudent.edad,
                func.count(models.PredictedStudent.edad).label("AMOUNT")
            )\
            .filter(models.PredictedStudent.estado == 1)\
            .group_by(models.PredictedStudent.edad)\
            .order_by(models.PredictedStudent.edad.asc())\
            .all()

    return(not_dropout, dropout)


def get_statistics_stratum(db: Session):
    """ 
    Fetch student statistics by stratum
    """     

    not_dropout = db.query(models.PredictedStudent.estrato, 
                    func.count(models.PredictedStudent.estrato).label("AMOUNT")
                )\
                .filter(models.PredictedStudent.estado == 0)\
                .group_by(models.PredictedStudent.estrato)\
                .order_by(models.PredictedStudent.estrato.asc())\
                .all()
            
    dropout = db.query(models.PredictedStudent.estrato,
                func.count(models.PredictedStudent.estrato).label("AMOUNT")
            )\
            .filter(models.PredictedStudent.estado == 1)\
            .group_by(models.PredictedStudent.estrato)\
            .order_by(models.PredictedStudent.estrato.asc())\
            .all()

    return(not_dropout, dropout)


def get_statistics_general(db: Session, fields: List = None, query_filter = None):
    """ 
    Fetch general statistics based on year and state
    """    

    if query_filter:
        query_filter = query_filter
    else:
        query_filter = {}

    if fields:
        fields = fields
    else:
        fields = ["anyo", "estrato", "estado"]

    return db.query(models.Students)\
            .options(load_only(*fields))\
            .filter(models.Students.anyo < 2022)\
            .filter_by(**query_filter).all()