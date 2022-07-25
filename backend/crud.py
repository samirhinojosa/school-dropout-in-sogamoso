from curses import pair_content
from sqlalchemy.orm import Session
import models


def get_predicted_students_id(db: Session, skip: int = 0, limit: int = 10):
    # return db.query(models.PredictedStudent.per_id).offset(skip).limit(limit).all()
    result =  db.query(models.PredictedStudent)\
                .with_entities(models.PredictedStudent.per_id)\
                .offset(skip).limit(limit).all()

    STUDENTS_ID = [id[0] for id in result]

    return STUDENTS_ID


def get_predicted_student_detail(db: Session, id: int):
    """ 
    Fetch a single student by ID
    """ 

    result = db.query(models.PredictedStudent)\
                .with_entities(models.PredictedStudent.per_id, models.PredictedStudent.genero,
                    models.PredictedStudent.edad, models.PredictedStudent.institucion,
                    models.PredictedStudent.grado_cod, models.PredictedStudent.jornada,
                    models.PredictedStudent.estrato, models.PredictedStudent.discapacidad,
                    models.PredictedStudent.pais_origen, models.PredictedStudent.idx) \
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