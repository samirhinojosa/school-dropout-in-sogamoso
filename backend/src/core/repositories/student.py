from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, asc
from src.configs.database import get_db
import src.core.models.predicted_student as pre_stu


class StudentRepository:


    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db


    def get_students_id(self, skip: Optional[int] = 0, limit: Optional[int] = 1000) -> list:
        """ 
        Fetch all students id

        Parameters:
            skip (int): Pagination starting.
            limit (int): End of pagination.
            
        Returns:
            ids (list) : List of students id.
        """ 

        result =  self.db.query(pre_stu.PredictedStudent)\
                    .with_entities(pre_stu.PredictedStudent.per_id)\
                    .offset(skip).limit(limit).all()

        STUDENTS_ID = [id[0] for id in result]

        
        return STUDENTS_ID

        
    def get_student_summary_by_id(self, id: int) -> list:
        """ 
        Fetch a summary student based on id

        Parameters:
            id (int): Student id.
            
        Returns:
            student (list) : Summary student.
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

        Parameters:
            id (int): Student id.
            
        Returns:
            student (list) : Student data necessary to predict.
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


    def get_statistics_age(self) -> list:
        """ 
        Fetch student statistics by age

        Returns:
            not_dropout (list) : Student age statistics who do not drop out.
            dropout (list) : Student age statistics who drop out.
        """ 

        not_dropout = self.db.query(pre_stu.PredictedStudent.edad,
                        func.count(pre_stu.PredictedStudent.edad).label("AMOUNT")
                    )\
                    .filter(pre_stu.PredictedStudent.estado == 0)\
                    .group_by(pre_stu.PredictedStudent.edad)\
                    .order_by(pre_stu.PredictedStudent.edad.asc())\
                    .all()
            
        dropout = self.db.query(pre_stu.PredictedStudent.edad,
                    func.count(pre_stu.PredictedStudent.edad).label("AMOUNT")
                )\
                .filter(pre_stu.PredictedStudent.estado == 1)\
                .group_by(pre_stu.PredictedStudent.edad)\
                .order_by(pre_stu.PredictedStudent.edad.asc())\
                .all()

        return(not_dropout, dropout)


    def get_statistics_stratum(self) -> list:
        """ 
        Fetch student statistics by stratum

        Returns:
            not_dropout (list) : Student stratum statistics who do not drop out.
            dropout (list) : Student stratum statistics who drop out.
        """ 

        not_dropout = self.db.query(pre_stu.PredictedStudent.estrato,
                        func.count(pre_stu.PredictedStudent.estrato).label("AMOUNT")
                    )\
                    .filter(pre_stu.PredictedStudent.estado == 0)\
                    .group_by(pre_stu.PredictedStudent.estrato)\
                    .order_by(pre_stu.PredictedStudent.estrato.asc())\
                    .all()
            
        dropout = self.db.query(pre_stu.PredictedStudent.estrato,
                    func.count(pre_stu.PredictedStudent.estrato).label("AMOUNT")
                )\
                .filter(pre_stu.PredictedStudent.estado == 1)\
                .group_by(pre_stu.PredictedStudent.estrato)\
                .order_by(pre_stu.PredictedStudent.estrato.asc())\
                .all()

        return(not_dropout, dropout)