from fastapi import FastAPI, APIRouter
from src.api.api_v1.api import api_router
from src.configs.settings import get_settings

# Runtime Settings/Environment Configuration
settings = get_settings()

description = """
This project is part of [Data Science 4 All - DS4A](https://www.correlation-one.com/data-science-for-all-colombia) \
training 🚀, and has two main objectives:

<ul style="list-style-type:disc;">
    <li>
        Building a classification model that will give a prediction about the probability of a student dropouts the school.<br>
        The model will be treated as a <strong>binary classification problem</strong>. So, 0 will be the class who does not
        dropout the school and 1 will be the class who dropouts the school.
    </li>
    <li>
        Build an interactive <strong>dashboard</strong> for <a href="https://www.sogamoso-boyaca.gov.co/" target="blank">Sogamoso municipality</a> 
        to interpret the predictions made by the model, and improve the  knowledge to allows the making-decision.
    </li>
</ul>
"""

app = FastAPI(
    title="School dropout Sogamoso - Backend",
    description=description,
    version=settings.FAST_API_VERSION,
    openapi_url="/openapi.json",
    contact={
        "name": "Samir Hinojosa",
        "url": "https://www.samirhinojosa.com/",
        "email": "samirhinojosa@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)


app.include_router(api_router, prefix=settings.API_VERSION)
api_router = APIRouter()




##########################################################

# @api_router.get("/api/predictions/students/{id}", status_code=200)
# async def get_student_prediction(id: int, db: Session = Depends(get_db)) -> dict:
#     """ 
#     Fetch the probability drop out of a student
#     """ 

#     student_prediction = crud.get_student_prediction(db, id=id)

#     if student_prediction is None:
#         raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
    
#     return student_prediction


# @api_router.get("/api/statistics/age/", status_code=200)
# async def get_statistics_age(db: Session = Depends(get_db)) -> dict:
#     """ 
#     Fetch student statistics by age XXXX
#     """ 

#     statistics = crud.get_statistics_age(db)

#     if statistics is None:
#         raise HTTPException(status_code=404, detail=f"Statistics age not found")

#     return {"ages_not_dropout" : statistics[0], "ages_dropout" : statistics[1]}


# @api_router.get("/api/statistics/stratum/", status_code=200)
# async def get_statistics_stratum(db: Session = Depends(get_db)) -> dict:
#     """ 
#     Fetch student statistics by stratum
#     """ 

#     statistics = crud.get_statistics_stratum(db)

#     if statistics is None:
#         raise HTTPException(status_code=404, detail=f"Statistics stratum not found")

#     return {"stratums_not_dropout" : statistics[0], "stratums_dropout" : statistics[1]}


# @api_router.get("/api/statistics/general/", status_code=200)
# def get_statistics_general(db: Session = Depends(get_db), fields: List[str] = Query(None)):
#     data = crud.get_statistics_general(db, fields=fields)
#     return data



#@app.get("/api/predictions/shap/students/{id}", status_code=200)
#async def read_student_by_id(id: int, db: Session = Depends(get_db)) -> dict:
#    """ 
#    Fetch student data based on id, to plot the local interpretation with SHAP
#    """ 
#
#    student = crud.get_student_by_id(db, id=id)
#
#   if student is None:
#        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
#    
#    return student


# registering the router
# app.include_router(api_router)
