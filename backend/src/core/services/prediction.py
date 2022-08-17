import os
from typing import Optional
from fastapi import Depends, HTTPException
import pandas as pd
import joblib
from src.core.repositories.student import StudentRepository


class StudentPredictionService:


    def __init__(self, student_repository: StudentRepository = Depends()) -> None:
        self.student_repository = student_repository


    def get_student_data_to_predict_by_id(self, id: int) -> dict:
        """ 
        Fetch data student to predict based on id

        Parameters:
            id (int): Student id.
            
        Returns:
            student (dict) : Student data necessary to predict.
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


    def get_student_prediction_by_id(self, id: int) -> dict:
        """ 
        Fetch student prediction based on id

        Parameters:
            id (int): Student id.
            
        Returns:
            student (dict) : Student prediction.
        """ 

        student = self.get_student_data_to_predict_by_id(id)

        if student is None:
            raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
        else:
            threshold = 0.632

            # loading the model
            path = os.path.abspath(os.pardir) + "/app/pickles/" 
            model = joblib.load(path + "model_20220706.pkl")

            # predicting
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