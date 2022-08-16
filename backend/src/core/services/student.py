from typing import Optional
from fastapi import Depends, HTTPException
from src.core.repositories.student import StudentRepository


class StudentService:


    def __init__(self, student_repository: StudentRepository = Depends()) -> None:
        self.student_repository = student_repository


    def get_students_id(self, skip: Optional[int] = 0, limit: Optional[int] = 1000) -> dict:
        """ 
        Fetch all students id

        Parameters:
            skip (int): Dataset to analyze.
            
        Returns:
            memory_usage (string) : The dataset's size on memory.
        """ 

        return {
            "ids" : self.student_repository.get_students_id(skip=skip, limit=limit)
        }  

    
    def get_student_summary_by_id(self, id: int) -> dict:
        """ 
        Fetch a summary student based on id
        """ 

        result = self.student_repository.get_student_summary_by_id(id)

        if result is None:
            raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
        else:
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

    
    def get_student_data_to_predict_by_id(self, id: int) -> dict:
        """ 
        Fetch data student to predict based on id
        """ 

        result = self.student_repository.get_student_data_to_predict_by_id(id)

        if result is None:
            raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
        else:

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
