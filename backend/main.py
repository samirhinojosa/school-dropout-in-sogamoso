from fastapi import FastAPI, APIRouter, HTTPException
from typing import Optional
from schemas import Student

app = FastAPI(
    title="School dropout Sogamoso - Backend",
    description="""descrpition""",
    version="1.0.0",
    openapi_url="/openapi.json"
)

api_router = APIRouter()


########################################################
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
import pandas as pd

df_students_to_predict = pd.read_csv("datasets/df_students_2022_predicted.csv")

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
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX





########################################################
# EndPoints
########################################################
@api_router.get("/api/students", status_code=200)
async def students_id() -> dict:
    """ 
    Fetch all students id
    """
    
    students_id = df_students_to_predict["PER_ID"].tolist()

    return {"StudentsId": students_id}


@api_router.get("/api/students/{student_id}", status_code=200, response_model=Student)
async def student_details(*, student_id: int) -> dict:
    """ 
    Fetch a single student by ID
    """ 

    df_student = df_students_to_predict[COLUMNS_DETAILS][df_students_to_predict["PER_ID"] == student_id]

    if df_student.shape[0] > 0:
        idx = df_students_to_predict[df_students_to_predict["PER_ID"]==student_id].index[0]

        for col in df_student.columns:
            globals()[col] = df_student.iloc[0, df_student.columns.get_loc(col)]
        
        student = {
            "id" : int(PER_ID),
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

    else:
        raise HTTPException(
            status_code=404, detail=f"Student with ID {student_id} not found"
        )

    return student


@api_router.get("/api/statistics/", status_code=200)
async def statistics(keyword: Optional[str] = "EDAD") -> dict:
    """ 
    Search for statistics based on label keyword
    """

    data_not_dropout = df_students_to_predict[df_students_to_predict["ESTADO"]==0].groupby(keyword).size()
    data_not_dropout = pd.DataFrame(data_not_dropout).reset_index()
    data_not_dropout.columns = [keyword, "AMOUNT"]
    data_not_dropout = data_not_dropout.set_index(keyword).to_dict()["AMOUNT"]

    data_dropout = df_students_to_predict[df_students_to_predict["ESTADO"]==1].groupby(keyword).size()
    data_dropout = pd.DataFrame(data_dropout).reset_index()
    data_dropout.columns = [keyword, "AMOUNT"]
    data_dropout = data_dropout.set_index(keyword).to_dict()["AMOUNT"]

    return {"not_dropout" : data_not_dropout, "dropout" : data_dropout}


# registering the router
app.include_router(api_router)