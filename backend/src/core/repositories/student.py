from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from src.configs.database import get_db
import src.core.models.predicted_student as pre_stu


class StudentRepository:


    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db


    def get_students_id(self, skip: Optional[int] = 0, limit: Optional[int] = 1000) -> list:
        """ 
        Fetch all students id
        """ 

        result =  self.db.query(pre_stu.PredictedStudent)\
                    .with_entities(pre_stu.PredictedStudent.per_id)\
                    .offset(skip).limit(limit).all()

        STUDENTS_ID = [id[0] for id in result]

        
        return STUDENTS_ID

        
    def get_student_summary_by_id(self, id: int) -> list:
        """ 
        Fetch a summary student based on id
        """ 

        result = self.db.query(pre_stu.PredictedStudent)\
                    .with_entities(
                        pre_stu.PredictedStudent.per_id, pre_stu.PredictedStudent.genero,
                        pre_stu.PredictedStudent.edad, pre_stu.PredictedStudent.institucion,
                        pre_stu.PredictedStudent.grado_cod, pre_stu.PredictedStudent.jornada,
                        pre_stu.PredictedStudent.estrato, pre_stu.PredictedStudent.discapacidad,
                        pre_stu.PredictedStudent.pais_origen, pre_stu.PredictedStudent.idx
                    )\
                    .filter(pre_stu.PredictedStudent.per_id == id).first()
    
        return result

    def get_student_data_to_predict_by_id(self, id: int) -> list:
        """ 
        Fetch data student to predict based on id
        """ 

        result = self.db.query(pre_stu.PredictedStudent)\
                    .with_entities(
                        pre_stu.PredictedStudent.institucion, pre_stu.PredictedStudent.genero,
                        pre_stu.PredictedStudent.jornada, pre_stu.PredictedStudent.pais_origen,
                        pre_stu.PredictedStudent.discapacidad, pre_stu.PredictedStudent.srpa,
                        pre_stu.PredictedStudent.institucion_sector, pre_stu.PredictedStudent.institucion_modelo,
                        pre_stu.PredictedStudent.institucion_apoyo_academico_especial, 
                        pre_stu.PredictedStudent.institucion_zona, pre_stu.PredictedStudent.institucion_caracter,
                        pre_stu.PredictedStudent.institucion_estado, 
                        pre_stu.PredictedStudent.institucion_prestador_de_servicio,
                        pre_stu.PredictedStudent.edad_clasificacion, pre_stu.PredictedStudent.grado_cod,
                        pre_stu.PredictedStudent.estrato, pre_stu.PredictedStudent.institucion_tamanyo,
                        pre_stu.PredictedStudent.institucion_numero_de_sedes, 
                        pre_stu.PredictedStudent.institucion_nivel_basica_primaria,
                        pre_stu.PredictedStudent.institucion_nivel_secundaria_primaria,
                        pre_stu.PredictedStudent.institucion_nivel_media, 
                        pre_stu.PredictedStudent.institucion_nivel_preescolar,
                        pre_stu.PredictedStudent.institucion_nivel_primera_infancia,
                        pre_stu.PredictedStudent.institucion_especialidad_academica,
                        pre_stu.PredictedStudent.institucion_especialidad_agropecuario,
                        pre_stu.PredictedStudent.institucion_especialidad_comercial,
                        pre_stu.PredictedStudent.institucion_especialidad_industrial,
                        pre_stu.PredictedStudent.institucion_especialidad_no_aplica,
                        pre_stu.PredictedStudent.institucion_especialidad_otro,
                        pre_stu.PredictedStudent.idx
                    )\
                    .filter(pre_stu.PredictedStudent.per_id == id).first()

        return result

